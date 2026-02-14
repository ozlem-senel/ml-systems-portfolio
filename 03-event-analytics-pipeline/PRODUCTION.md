# Production Deployment Guide

## Overview
This document describes the production-ready features of the Event Analytics Pipeline and provides guidance for deploying in a production environment.

## Production Features

### 1. Enhanced ETL Pipeline (`etl_pipeline_prod.py`)

**Error Handling**
- Comprehensive try-catch blocks throughout the pipeline
- Custom `DataQualityError` exception for data validation failures
- Graceful handling of malformed JSON lines (tracks failed events)
- Maximum failure threshold (100 failed lines before aborting)

**Logging**
- Multi-handler logging (file + console output)
- Structured log messages with timestamps and log levels
- Log file stored in `logs/etl_pipeline.log`
- Progress tracking for long-running operations

**Data Quality Checks**
- Minimum event count validation
- Required event type verification (session_start, session_end)
- Null percentage monitoring per column
- Duplicate event detection
- Future timestamp detection
- Configurable strict mode (warnings vs. errors)

**Configuration Management**
- YAML-based configuration (`config/etl_config.yaml`)
- Externalized quality check thresholds
- Environment-specific settings support
- Fallback to defaults if config missing

**Monitoring & Metrics**
- Events loaded/cleaned/failed counters
- Processing time tracking
- Throughput calculation (events/second)
- Pipeline execution summary

### 2. Configuration System

**Quality Checks** (`config/etl_config.yaml`)
```yaml
quality_checks:
  min_events: 1000                    # Minimum events required
  max_null_percentage: 0.1            # 10% null threshold
  required_event_types:               # Must be present
    - session_start
    - session_end
  max_future_days: 1                  # Max days in future
```

**Aggregation Settings**
```yaml
aggregation:
  min_dau: 1                          # Minimum daily active users
  max_revenue_per_event: 1000         # Outlier detection threshold
```

**Monitoring**
```yaml
monitoring:
  enable_alerts: false                # Alert system integration
  log_level: INFO                     # DEBUG, INFO, WARNING, ERROR
strict_mode: false                    # Fail on warnings
```

### 3. Testing Framework

**Unit Tests** (`tests/test_etl_pipeline.py`)
- Event loading and parsing tests
- Input file validation tests  
- Data quality check verification
- Error handling coverage
- 4 passing tests covering core functionality

**Test Execution**
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_etl_pipeline.py::TestEventETLPipeline::test_load_events_success -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Deployment Checklist

### Pre-Deployment

- Review and customize `config/etl_config.yaml` for your environment
- Set appropriate quality check thresholds
- Configure log levels (DEBUG for testing, INFO for production)
- Test with representative sample data
- Run unit tests to verify functionality
- Set up log rotation for `logs/etl_pipeline.log`

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import polars, yaml; print('Dependencies OK')"
```

### Data Preparation

**Input Requirements**
- Format: JSONL (newline-delimited JSON)
- Required fields: `event_id`, `player_id`, `event_type`, `timestamp`
- Optional fields: `session_id`, `properties` (dict)
- Timestamp format: ISO 8601 (YYYY-MM-DDTHH:MM:SS)

**Example Event**
```json
{
  "event_id": "evt_12345",
  "player_id": "player_67890",
  "session_id": "session_abc",
  "event_type": "session_start",
  "timestamp": "2024-01-15T14:30:00",
  "properties": {
    "device_type": "mobile",
    "country": "US",
    "app_version": "2.1.0"
  }
}
```

### Running the Pipeline

**Command Line**
```bash
python src/etl_pipeline_prod.py \
  --input data/raw_events/events_*.jsonl \
  --output data/processed \
  --config config/etl_config.yaml
```

**Programmatic Usage**
```python
from src.etl_pipeline_prod import EventETLPipeline

# Initialize pipeline
pipeline = EventETLPipeline(
    input_file="data/raw_events/events.jsonl",
    config_path="config/etl_config.yaml"
)

# Validate input
pipeline.validate_input_file()

# Run pipeline
pipeline.run(output_dir="data/processed")

# Check metrics
print(f"Processed {pipeline.metrics['events_loaded']} events")
print(f"Throughput: {pipeline.metrics['throughput']:.0f} events/sec")
```

### Monitoring

**Log Monitoring**
```bash
# Real-time log monitoring
tail -f logs/etl_pipeline.log

# Check for errors
grep ERROR logs/etl_pipeline.log

# Check for data quality warnings
grep "Quality check found" logs/etl_pipeline.log
```

**Metrics Tracking**
- Monitor `events_failed` counter (should be close to 0)
- Track `throughput` for performance regression
- Alert on `processing_time_seconds` exceeding SLA
- Verify `events_loaded` matches expected volume

### Production Best Practices

**Scheduling**
```bash
# Cron job example (daily at 2 AM)
0 2 * * * cd /path/to/project && /path/to/venv/bin/python src/etl_pipeline_prod.py --input data/raw_events/events_$(date +\%Y\%m\%d).jsonl --output data/processed --config config/etl_config.yaml >> logs/cron.log 2>&1
```

**Resource Management**
- Polars uses lazy evaluation and streaming for memory efficiency
- For large datasets (>10M events), consider batching by date
- Monitor memory usage with `htop` or similar tools
- Set `infer_schema_length` appropriately (default: 10000)

**Error Recovery**
- Pipeline is idempotent (can safely re-run)
- Failed runs don't corrupt existing output
- Check logs for specific failure reasons
- Validate input data format before running

**Security**
- Restrict file permissions on config files (`chmod 600 config/etl_config.yaml`)
- Use environment variables for sensitive settings
- Implement access controls on data directories
- Audit log access in production

**Scalability**
- Current implementation: Single-node processing
- For distributed processing: Consider Apache Spark or Dask
- Horizontal scaling: Partition input by date/shard
- Vertical scaling: Increase memory, use faster disks

## Performance Benchmarks

**Test Environment**
- MacBook Pro, M1 chip, 16GB RAM
- Python 3.12, Polars 0.20

**Results**
- 940K events processed in 8.4 seconds
- Throughput: ~112K events/second
- Memory usage: ~500MB peak
- Output files: 3 Parquet files (31 days, 27 cohorts)

## Troubleshooting

**Common Issues**

1. **FileNotFoundError: logs directory**
   - Fixed in production pipeline (auto-creates logs/ directory)
   
2. **ColumnNotFoundError: player_id**
   - Ensure input events have required fields
   - Check field name spelling (case-sensitive)
   
3. **DataQualityError: too few events**
   - Lower `min_events` threshold in config
   - Or set `strict_mode: false` to treat as warning
   
4. **High null percentages**
   - Expected for event-specific properties (sparse columns)
   - Adjust `max_null_percentage` threshold
   - Review data generation logic

5. **Future timestamps detected**
   - Clock skew between data sources
   - Timezone conversion issues
   - Adjust `max_future_days` if legitimate

**Debug Mode**
```bash
# Enable debug logging
export POLARS_VERBOSE=1

# Run with debug config
python src/etl_pipeline_prod.py --config config/etl_config_debug.yaml
```

## Support & Maintenance

**Regular Maintenance**
- Weekly: Review logs for warnings
- Monthly: Analyze quality check trends
- Quarterly: Performance benchmarking
- Annually: Dependency updates

**Contact**
For questions or issues, check:
- Project README.md
- QUICKSTART.md for basic usage
- GitHub Issues (if applicable)
- Internal documentation wiki

---

**Last Updated:** 2024-01-15  
**Pipeline Version:** 1.0.0  
**Maintainer:** Data Engineering Team
