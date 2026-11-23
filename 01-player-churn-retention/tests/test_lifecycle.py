import importlib.util
from pathlib import Path

import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location('lifecycle', Path(__file__).parents[1] / 'src' / 'lifecycle.py')
lifecycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lifecycle)


def test_windows_and_maturity():
    events = pd.DataFrame([
        ('a', 'session_start', '2026-01-01', None),
        ('a', 'purchase', '2026-01-07', 2.0),
        ('a', 'purchase', '2026-01-08', 5.0),
        ('a', 'purchase', '2026-01-22', 99.0),
        ('b', 'session_start', '2026-01-20', None),
        ('x', 'session_start', '2026-01-23', None),
    ], columns=['player_id', 'event_type', 'timestamp', 'prop_price_usd'])
    data = lifecycle.make_dataset(events)
    assert list(data.index) == ['a']
    assert data.loc['a', 'revenue'] == 2
    assert data.loc['a', 'future_revenue'] == 5
    assert data.loc['a', 'future_payer'] == 1


def test_purchase_field_cannot_silently_disappear():
    events = pd.DataFrame([('a', 'purchase', '2026-01-01')], columns=['player_id', 'event_type', 'timestamp'])
    with pytest.raises(ValueError, match='prop_price_usd'):
        lifecycle.make_dataset(events)
