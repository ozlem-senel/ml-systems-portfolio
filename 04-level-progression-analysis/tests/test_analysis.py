import importlib.util
from pathlib import Path

import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location('analysis', Path(__file__).parents[1] / 'src' / 'analysis.py')
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def event(event_id, player, attempt, kind, date):
    return dict(event_id=event_id, player_id=player, prop_attempt_id=attempt,
                prop_level=1, event_type=kind, timestamp=pd.Timestamp(date))


def test_metrics_respect_first_attempt_and_observation_window():
    events = pd.DataFrame([
        event('1', 'a', 'a1', 'level_start', '2026-01-01'),
        event('2', 'a', 'a1', 'level_fail', '2026-01-01'),
        event('3', 'a', 'a2', 'level_start', '2026-01-02'),
        event('4', 'a', 'a2', 'level_complete', '2026-01-02'),
        event('5', 'b', 'b1', 'level_start', '2026-01-01'),
        event('6', 'b', 'b1', 'level_fail', '2026-01-01'),
        event('7', 'c', 'c1', 'level_start', '2026-01-09'),
        event('8', 'c', 'c1', 'level_fail', '2026-01-09'),
        event('9', 'x', None, 'session_end', '2026-01-10'),
    ])
    row = analysis.level_metrics(events).iloc[0]
    assert row.players_started == 3
    assert row.completion_rate == pytest.approx(1 / 3)
    assert row.first_attempt_win_rate == 0
    assert row.mature_players == 2
    assert row.abandonment_rate == pytest.approx(0.5)


def test_legacy_data_has_actionable_error():
    with pytest.raises(ValueError, match='attempt IDs'):
        analysis.build_attempts(pd.DataFrame(columns=['event_id', 'player_id', 'event_type', 'timestamp', 'prop_level']))


def test_date_filter_selects_first_start_and_censors_later_outcomes():
    events = pd.DataFrame([
        event('1', 'a', 'a1', 'level_start', '2026-01-01'),
        event('2', 'a', 'a1', 'level_fail', '2026-01-01'),
        event('3', 'a', 'a2', 'level_start', '2026-01-03'),
        event('4', 'a', 'a2', 'level_complete', '2026-01-03'),
        event('5', 'b', 'b1', 'level_start', '2026-01-02'),
        event('6', 'b', 'b1', 'level_complete', '2026-01-04'),
        event('7', 'c', 'c1', 'level_start', '2026-01-03'),
        event('8', 'c', 'c1', 'level_complete', '2026-01-03'),
    ])
    row = analysis.level_metrics(events, start_date='2026-01-02', end_date='2026-01-03').iloc[0]
    assert row.players_started == 2  # a started before the interval
    assert row.completion_rate == 0.5  # b completed after its end
    assert row.first_attempt_win_rate == 0.5
    assert row.mean_attempts == 1


def test_funnel_and_retry_after_failure_including_same_timestamp():
    events = pd.DataFrame([
        event('1', 'a', 'a1', 'level_start', '2026-01-01'),
        event('2', 'a', 'a1', 'level_fail', '2026-01-02'),
        event('3', 'a', 'a2', 'level_start', '2026-01-02'),
        event('4', 'a', 'a2', 'level_complete', '2026-01-03'),
        dict(event('5', 'a', 'a3', 'level_start', '2026-01-04'), prop_level=2),
        event('6', 'b', 'b1', 'level_start', '2026-01-01'),
        event('7', 'b', 'b1', 'level_fail', '2026-01-02'),
        event('8', 'x', None, 'session_end', '2026-01-12'),
    ])
    row = analysis.level_metrics(events).query('level == 1').iloc[0]
    assert (row.players_started, row.players_completed, row.next_level_players) == (2, 1, 1)
    assert (row.retry_eligible, row.retried_7d) == (2, 1)
    assert row.retry_rate_7d == 0.5


def test_prioritization_excludes_small_samples_and_detects_local_drop():
    metrics = pd.DataFrame({'level': [1, 2, 3, 4], 'players_started': [100, 100, 100, 5],
                            'first_wins': [80, 40, 80, 0],
                            'first_attempt_win_rate': [0.8, 0.4, 0.8, 0],
                            'first_win_ci_low': [0.7, 0.3, 0.7, 0],
                            'first_win_ci_high': [0.9, 0.5, 0.9, 1]})
    ranked = analysis.prioritize_levels(metrics)
    assert ranked.iloc[0]['level'] == 2
    assert ranked.iloc[0]['gap'] == pytest.approx(0.4)
    assert 4 not in ranked.level.values


def test_progression_funnel_tracks_same_cohort_in_order_and_censors_dates():
    def start(event_id, player, level, day):
        return dict(event(event_id, player, event_id, 'level_start', day), prop_level=level)
    events = pd.DataFrame([
        start('a1', 'a', 1, '2026-01-02'), start('a2', 'a', 2, '2026-01-03'),
        start('a3', 'a', 3, '2026-01-05'), start('b1', 'b', 1, '2026-01-02'),
        start('b3', 'b', 3, '2026-01-03'),
        start('c1', 'c', 1, '2026-01-01'), start('c2', 'c', 2, '2026-01-03'),
    ])
    funnel = analysis.progression_funnel(events, 1, 3, start_date='2026-01-02', end_date='2026-01-04')
    assert funnel.players.tolist() == [2, 1, 0]
    assert funnel.share.tolist() == [1, .5, 0]
