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
