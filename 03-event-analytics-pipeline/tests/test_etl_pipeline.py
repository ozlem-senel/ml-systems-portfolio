"""
Unit tests for ETL pipeline
Tests data loading, transformation, and quality checks
"""
import pytest
import polars as pl
import yaml
from pathlib import Path
import json
from datetime import datetime, timedelta
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from etl_pipeline_prod import EventETLPipeline, DataQualityError


@pytest.fixture
def sample_events_file(tmp_path):
    """Create a temporary JSONL file with sample events"""
    events = []
    base_time = datetime(2024, 1, 1, 12, 0, 0)
    
    # Create 100 sample events
    for i in range(100):
        event = {
            'event_id': f'evt_{i}',
            'player_id': f'player_{i % 20}',  # 20 unique players
            'session_id': f'session_{i % 50}',
            'event_type': ['session_start', 'session_end', 'level_complete'][i % 3],
            'timestamp': (base_time + timedelta(hours=i)).isoformat(),
            'properties': {
                'device_type': 'mobile',
                'country': 'US'
            }
        }
        events.append(event)
    
    # Write to JSONL
    events_file = tmp_path / "test_events.jsonl"
    with open(events_file, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')
    
    return events_file


@pytest.fixture
def etl_config():
    """Create a test configuration"""
    return {
        'quality_checks': {
            'min_events': 10,
            'max_null_percentage': 0.5,
            'required_event_types': ['session_start'],
            'check_duplicates': True,
            'check_future_timestamps': True,
            'max_future_days': 1
        },
        'aggregation': {
            'min_dau': 1,
            'max_revenue_per_event': 1000
        },
        'strict_mode': False
    }


@pytest.fixture
def etl_config_file(tmp_path, etl_config):
    """Create a temporary config file"""
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(etl_config, f)
    return config_file


class TestEventETLPipeline:
    
    def test_load_events_success(self, sample_events_file, etl_config_file, tmp_path):
        """Test successful event loading"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        df = pipeline.load_events()
        
        assert df is not None
        assert len(df) == 100
        assert 'event_id' in df.columns
        assert 'player_id' in df.columns
        assert 'event_type' in df.columns
        assert 'timestamp' in df.columns
        assert 'prop_device_type' in df.columns
        assert 'prop_country' in df.columns
    
    def test_load_events_nonexistent_file(self, tmp_path, etl_config_file):
        """Test loading from nonexistent file"""
        pipeline = EventETLPipeline(
            str(tmp_path / 'nonexistent.jsonl'),
            str(etl_config_file)
        )
        
        with pytest.raises(FileNotFoundError):
            pipeline.load_events()
    
    def test_validate_input_file(self, sample_events_file, etl_config_file, tmp_path):
        """Test input file validation"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        # Should not raise exception
        pipeline.validate_input_file()
    
    def test_validate_input_file_missing(self, tmp_path, etl_config_file):
        """Test validation fails for missing file"""
        pipeline = EventETLPipeline(
            str(tmp_path / 'missing.jsonl'),
            str(etl_config_file)
        )
        
        with pytest.raises(FileNotFoundError):
            pipeline.validate_input_file()
    
    def test_quality_checks_pass(self, sample_events_file, etl_config_file, tmp_path):
        """Test that quality checks pass for valid data"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        df = pipeline.load_events()
        issues = pipeline.run_quality_checks(df)
        
        # Should have minimal issues for this clean test data
        assert isinstance(issues, list)
    
    def test_quality_checks_fail_min_events(self, tmp_path, etl_config):
        """Test quality check fails when too few events"""
        # Create file with only 5 events (less than min_events: 10)
        events = []
        for i in range(5):
            event = {
                'event_id': f'evt_{i}',
                'player_id': f'player_{i}',
                'session_id': f'session_{i}',
                'event_type': 'session_start',
                'timestamp': datetime.now().isoformat(),
                'properties': {}
            }
            events.append(event)
        
        events_file = tmp_path / "few_events.jsonl"
        with open(events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
        
        # Set strict mode to raise errors
        strict_config = etl_config.copy()
        strict_config['strict_mode'] = True
        
        # Create config file
        config_file = tmp_path / "strict_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(strict_config, f)
        
        pipeline = EventETLPipeline(
            str(events_file),
            str(config_file)
        )
        
        df = pipeline.load_events()
        
        with pytest.raises(DataQualityError, match="too few events"):
            pipeline.run_quality_checks(df)
    
    def test_quality_checks_missing_required_event_types(self, tmp_path, etl_config):
        """Test quality check fails when required event types are missing"""
        # Create events without session_start
        events = []
        for i in range(20):
            event = {
                'event_id': f'evt_{i}',
                'player_id': f'player_{i}',
                'session_id': f'session_{i}',
                'event_type': 'level_complete',  # No session_start
                'timestamp': datetime.now().isoformat(),
                'properties': {}
            }
            events.append(event)
        
        events_file = tmp_path / "no_session_start.jsonl"
        with open(events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
        
        strict_config = etl_config.copy()
        strict_config['strict_mode'] = True
        
        # Create config file
        config_file = tmp_path / "strict_config2.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(strict_config, f)
        
        pipeline = EventETLPipeline(
            str(events_file),
            str(config_file)
        )
        
        df = pipeline.load_events()
        
        with pytest.raises(DataQualityError, match="Missing required event types"):
            pipeline.run_quality_checks(df)
    
    def test_clean_and_enrich_data(self, sample_events_file, etl_config_file, tmp_path):
        """Test data cleaning and enrichment"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        df = pipeline.load_events()
        cleaned_df = pipeline.clean_and_enrich_data(df)
        
        assert cleaned_df is not None
        assert 'date' in cleaned_df.columns
        assert 'hour' in cleaned_df.columns
        assert 'day_of_week' in cleaned_df.columns
        
        # Check that timestamps were converted to datetime
        assert cleaned_df['timestamp'].dtype == pl.Datetime
    
    def test_aggregate_daily_metrics(self, sample_events_file, etl_config_file, tmp_path):
        """Test daily metrics aggregation"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        df = pipeline.load_events()
        cleaned_df = pipeline.clean_and_enrich_data(df)
        daily_metrics = pipeline.aggregate_daily_metrics(cleaned_df)
        
        assert daily_metrics is not None
        assert 'date' in daily_metrics.columns
        assert 'dau' in daily_metrics.columns
        assert 'total_events' in daily_metrics.columns
        
        # Check that DAU calculation is reasonable
        assert (daily_metrics['dau'] > 0).all()
        assert (daily_metrics['dau'] <= 20).all()  # We have 20 unique users
    
    def test_calculate_retention(self, sample_events_file, etl_config_file, tmp_path):
        """Test retention calculation"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        df = pipeline.load_events()
        cleaned_df = pipeline.clean_and_enrich_data(df)
        retention = pipeline.calculate_retention(cleaned_df)
        
        assert retention is not None
        assert 'cohort_date' in retention.columns
        assert 'day_number' in retention.columns
        assert 'users' in retention.columns
        assert 'retention_rate' in retention.columns
        
        # Retention rate should be between 0 and 1
        assert (retention['retention_rate'] >= 0).all()
        assert (retention['retention_rate'] <= 1).all()
    
    def test_full_pipeline_execution(self, sample_events_file, etl_config_file, tmp_path):
        """Test complete pipeline execution"""
        output_dir = tmp_path / 'output'
        
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        # Run full pipeline
        pipeline.run(str(output_dir))
        
        # Check that output files were created
        assert (output_dir / 'events_cleaned.parquet').exists()
        assert (output_dir / 'daily_metrics.parquet').exists()
        assert (output_dir / 'retention_cohorts.parquet').exists()
        
        # Verify output data can be loaded
        cleaned_events = pl.read_parquet(output_dir / 'events_cleaned.parquet')
        assert len(cleaned_events) == 100
        
        daily_metrics = pl.read_parquet(output_dir / 'daily_metrics.parquet')
        assert len(daily_metrics) > 0
        
        retention = pl.read_parquet(output_dir / 'retention_cohorts.parquet')
        assert len(retention) > 0
    
    def test_metrics_tracking(self, sample_events_file, etl_config_file, tmp_path):
        """Test that metrics are tracked correctly"""
        pipeline = EventETLPipeline(
            str(sample_events_file),
            str(etl_config_file)
        )
        
        pipeline.run(str(tmp_path / 'output'))
        
        # Check metrics
        assert pipeline.metrics['events_loaded'] == 100
        assert pipeline.metrics['events_cleaned'] == 100
        assert pipeline.metrics['events_failed'] == 0
        assert pipeline.metrics['processing_time_seconds'] > 0
        assert pipeline.metrics['throughput'] > 0


class TestDataQualityChecks:
    """Test suite for data quality validation"""
    
    def test_detect_duplicates(self, tmp_path, etl_config):
        """Test duplicate detection"""
        # Create events with duplicates
        events = []
        for i in range(10):
            event = {
                'event_id': 'duplicate_id',  # Same ID for all
                'player_id': f'player_{i}',
                'session_id': f'session_{i}',
                'event_type': 'session_start',
                'timestamp': datetime.now().isoformat(),
                'properties': {}
            }
            events.append(event)
        
        events_file = tmp_path / "duplicates.jsonl"
        with open(events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
        
        # Create config file
        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(etl_config, f)
        
        pipeline = EventETLPipeline(
            str(events_file),
            str(config_file)
        )
        
        df = pipeline.load_events()
        issues = pipeline.run_quality_checks(df)
        
        # Should detect duplicates
        duplicate_issues = [i for i in issues if 'duplicate' in i.lower()]
        assert len(duplicate_issues) > 0
    
    def test_detect_future_timestamps(self, tmp_path, etl_config):
        """Test future timestamp detection"""
        # Create events with future timestamps
        events = []
        future_time = datetime.now() + timedelta(days=365)
        
        for i in range(20):
            event = {
                'event_id': f'evt_{i}',
                'player_id': f'player_{i}',
                'session_id': f'session_{i}',
                'event_type': 'session_start',
                'timestamp': future_time.isoformat(),
                'properties': {}
            }
            events.append(event)
        
        events_file = tmp_path / "future.jsonl"
        with open(events_file, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
        
        # Create config file
        config_file = tmp_path / "config2.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(etl_config, f)
        
        pipeline = EventETLPipeline(
            str(events_file),
            str(config_file)
        )
        
        df = pipeline.load_events()
        issues = pipeline.run_quality_checks(df)
        
        # Should detect future timestamps
        future_issues = [i for i in issues if 'future' in i.lower()]
        assert len(future_issues) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
