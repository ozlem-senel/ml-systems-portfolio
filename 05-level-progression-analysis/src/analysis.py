"""Level metrics from the cleaned event pipeline; all results are descriptive."""
from pathlib import Path
import argparse
import pandas as pd


def build_attempts(events: pd.DataFrame) -> pd.DataFrame:
    required = {'event_id', 'player_id', 'event_type', 'timestamp', 'prop_level', 'prop_attempt_id'}
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(f"Missing {sorted(missing)}. Generate new events with attempt IDs and rerun ETL.")
    level = events.loc[events.event_type.isin(['level_start', 'level_complete', 'level_fail'])].copy()
    level = level.drop_duplicates('event_id')
    if level.empty or level.prop_attempt_id.isna().all():
        raise ValueError('No attempt IDs found. Generate new events and rerun ETL.')
    level['timestamp'] = pd.to_datetime(level['timestamp'])
    starts = level[level.event_type == 'level_start'].copy()
    ends = level[level.event_type.isin(['level_complete', 'level_fail'])].copy()
    # Ambiguous attempts must not be silently counted as valid.
    start_counts = starts.groupby('prop_attempt_id').size()
    end_counts = ends.groupby('prop_attempt_id').size()
    starts = starts[starts.prop_attempt_id.isin(start_counts[start_counts == 1].index)]
    ends = ends[ends.prop_attempt_id.isin(end_counts[end_counts == 1].index)]
    attempts = starts.merge(ends[['prop_attempt_id', 'player_id', 'prop_level', 'timestamp', 'event_type']],
                            on='prop_attempt_id', how='left', suffixes=('', '_end'), validate='one_to_one')
    valid_end = ((attempts.player_id == attempts.player_id_end) &
                 (attempts.prop_level == attempts.prop_level_end) &
                 (attempts.timestamp_end >= attempts.timestamp))
    attempts.loc[~valid_end, ['timestamp_end', 'event_type_end']] = pd.NA
    return attempts.sort_values(['player_id', 'prop_level', 'timestamp', 'prop_attempt_id'])


def level_metrics(events: pd.DataFrame, abandonment_days: int = 7) -> pd.DataFrame:
    attempts = build_attempts(events)
    if attempts.empty:
        raise ValueError('No valid level starts found.')
    # A player-level is observed from their first start through their last attempt.
    attempts['completed'] = attempts.event_type_end.eq('level_complete')
    grouped = attempts.groupby(['player_id', 'prop_level'], sort=False)
    players = grouped.agg(first_start=('timestamp', 'min'), last_start=('timestamp', 'max'),
                          attempts=('prop_attempt_id', 'size'), completed=('completed', 'max')).reset_index()
    first = grouped.head(1)[['player_id', 'prop_level', 'event_type_end']].rename(columns={'event_type_end': 'first_outcome'})
    players = players.merge(first, on=['player_id', 'prop_level'], validate='one_to_one')
    snapshot = pd.to_datetime(events.timestamp).max()
    players['mature'] = players.last_start <= snapshot - pd.Timedelta(days=abandonment_days)
    players['abandoned'] = players.mature & ~players.completed
    players['first_win'] = players.first_outcome.eq('level_complete')
    result = players.groupby('prop_level').agg(
        players_started=('player_id', 'size'), players_completed=('completed', 'sum'),
        first_wins=('first_win', 'sum'), median_attempts=('attempts', 'median'),
        mature_players=('mature', 'sum'), abandoned=('abandoned', 'sum')).reset_index()
    result['completion_rate'] = result.players_completed / result.players_started
    result['first_attempt_win_rate'] = result.first_wins / result.players_started
    result['abandonment_rate'] = result.abandoned / result.mature_players.replace(0, float('nan'))
    # Wilson interval for first-attempt win rate; display the sample size alongside it.
    n = result.players_started
    p = result.first_attempt_win_rate
    z = 1.96
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    margin = z * ((p*(1-p)/n + z*z/(4*n*n)) ** 0.5) / (1 + z*z/n)
    result['first_win_ci_low'] = (center - margin).clip(lower=0)
    result['first_win_ci_high'] = (center + margin).clip(upper=1)
    # Share of observed level starters who reached each level.
    result['reach_rate'] = result.players_started / players.player_id.nunique()
    return result.rename(columns={'prop_level': 'level'}).sort_values('level')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('reports/level_metrics.csv'))
    args = parser.parse_args()
    metrics = level_metrics(pd.read_parquet(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(args.output, index=False)
    print(f'Saved {len(metrics)} levels to {args.output}')


if __name__ == '__main__':
    main()
