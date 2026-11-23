"""Train lifecycle baselines on mature, event-derived player cohorts.

First seven observed days are features; the following fourteen days supply labels.
Revenue is a fixed-horizon proxy, not lifetime value.
"""
from pathlib import Path
import argparse
import json

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (average_precision_score, mean_absolute_error,
                             roc_auc_score, brier_score_loss)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ['sessions', 'active_days', 'level_starts', 'level_completions',
            'level_failures', 'ads', 'purchases', 'revenue']


def make_dataset(events, observation_days=7, horizon_days=14):
    required = {'player_id', 'event_type', 'timestamp'}
    if not required.issubset(events.columns):
        raise ValueError(f'Missing columns: {sorted(required - set(events.columns))}')
    events = events.copy()
    if 'prop_price_usd' not in events and events.event_type.eq('purchase').any():
        raise ValueError('Purchase events exist but prop_price_usd is missing; rerun the updated ETL.')
    events['timestamp'] = pd.to_datetime(events.timestamp)
    if 'event_id' in events:
        events = events.drop_duplicates('event_id')
    events = events.dropna(subset=['player_id', 'timestamp'])
    if events.empty:
        raise ValueError('No valid events.')
    # First observed activity is a proxy for install, not a true install event.
    first = events.groupby('player_id').timestamp.min().rename('first_seen')
    snapshot = events.timestamp.max()
    mature = first[first + pd.Timedelta(days=observation_days + horizon_days) <= snapshot]
    events = events.join(mature, on='player_id', how='inner')
    if events.empty:
        raise ValueError('No mature players: generate data covering more than 21 days.')
    age = (events.timestamp - events.first_seen).dt.total_seconds() / 86400
    observed = events[age < observation_days].copy()
    future = events[(age >= observation_days) & (age < observation_days + horizon_days)].copy()
    for frame in (observed, future):
        frame['amount'] = pd.to_numeric(frame.get('prop_price_usd', pd.Series(0, index=frame.index)), errors='coerce').fillna(0)
        frame.loc[frame.event_type != 'purchase', 'amount'] = 0
    observed['day'] = observed.timestamp.dt.floor('D')
    counts = pd.crosstab(observed.player_id, observed.event_type)
    dataset = mature.to_frame().join(counts, how='left').fillna(0)
    mapping = {'session_start': 'sessions', 'level_start': 'level_starts', 'level_complete': 'level_completions',
               'level_fail': 'level_failures', 'ad_watched': 'ads', 'purchase': 'purchases'}
    for source, target in mapping.items():
        dataset[target] = dataset[source] if source in dataset else 0
    dataset['active_days'] = observed.groupby('player_id').day.nunique()
    dataset['revenue'] = observed.groupby('player_id').amount.sum()
    dataset['future_revenue'] = future.groupby('player_id').amount.sum().reindex(dataset.index, fill_value=0)
    dataset['future_payer'] = (dataset.future_revenue > 0).astype(int)
    return dataset[['first_seen', *FEATURES, 'future_revenue', 'future_payer']]


def train_and_evaluate(dataset):
    # Entire cohorts stay on one side of the chronological split.
    cohort = pd.to_datetime(dataset.first_seen).dt.floor('D')
    dates = sorted(cohort.unique())
    if len(dates) < 2:
        raise ValueError('Need at least two mature first-seen dates for a chronological holdout.')
    cutoff = dates[min(len(dates) - 1, max(1, int(len(dates) * 0.8)))]
    # All training labels must be fully available before the first test cohort.
    train = dataset[dataset.first_seen + pd.Timedelta(days=21) <= cutoff]
    test = dataset[cohort >= cutoff]
    if len(train) < 10 or len(test) < 2:
        raise ValueError('Not enough mature players for training and holdout.')
    x_train, x_test = train[FEATURES], test[FEATURES]
    reg = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42, n_jobs=-1)
    baseline = DummyRegressor(strategy='mean')
    reg.fit(x_train, train.future_revenue)
    baseline.fit(x_train, train.future_revenue)
    results = {'train_players': len(train), 'test_players': len(test), 'test_first_seen_from': str(pd.Timestamp(cutoff).date()),
               'excluded_gap_players': len(dataset) - len(train) - len(test),
               'future_14d_revenue': {'mae': mean_absolute_error(test.future_revenue, reg.predict(x_test)),
                                      'baseline_mae': mean_absolute_error(test.future_revenue, baseline.predict(x_test))}}
    # Conversion is defined only among players who have not paid in the observation window.
    nonpay_train, nonpay_test = train[train.purchases == 0], test[test.purchases == 0]
    if nonpay_train.future_payer.nunique() == 2 and len(nonpay_test):
        classifier = RandomForestClassifier(n_estimators=100, min_samples_leaf=5, random_state=42, n_jobs=-1)
        classifier.fit(nonpay_train[FEATURES], nonpay_train.future_payer)
        probabilities = classifier.predict_proba(nonpay_test[FEATURES])[:, 1]
        labels = nonpay_test.future_payer
        conversion = {'test_players': len(labels), 'positive_players': int(labels.sum()), 'base_rate': float(labels.mean()),
                      'brier_score': brier_score_loss(labels, probabilities)}
        if labels.nunique() == 2:
            conversion.update(roc_auc=roc_auc_score(labels, probabilities), average_precision=average_precision_score(labels, probabilities))
        else:
            conversion['status'] = 'holdout has one class; discrimination metrics unavailable'
        results['first_payer_conversion'] = conversion
    else:
        results['first_payer_conversion'] = {'status': 'insufficient class variation or holdout players'}
    clustering = make_pipeline(StandardScaler(), KMeans(n_clusters=3, random_state=42, n_init=10))
    clustering.fit(x_train)
    segments = test.assign(segment=clustering.predict(x_test)).groupby('segment')[FEATURES].mean().round(2)
    results['holdout_segment_profiles'] = segments.to_dict(orient='index')
    results['holdout_segment_sizes'] = pd.Series(clustering.predict(x_test)).value_counts().sort_index().to_dict()
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('reports/lifecycle_results.json'))
    args = parser.parse_args()
    dataset = make_dataset(pd.read_parquet(args.input))
    results = train_and_evaluate(dataset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, default=str) + '\n')
    print(json.dumps(results, indent=2, default=str))


if __name__ == '__main__':
    main()
