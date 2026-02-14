# Game Event Analytics Pipeline - Quick Start

## Generate Events

```bash
cd 03-event-analytics-pipeline

# Install dependencies
pip install -r requirements.txt

# Generate synthetic game events
python src/event_generator.py --players 5000 --days 30
```

This creates realistic mobile game events in `data/raw_events/`.

## Run ETL Pipeline

```bash
# Process events into metrics
python src/etl_pipeline.py --input data/raw_events/events_*.jsonl
```

This creates:
- `data/processed/events_cleaned.parquet` - Cleaned events
- `data/processed/daily_metrics.parquet` - Daily aggregated metrics
- `data/processed/retention_cohorts.parquet` - Retention analysis

## Launch Dashboard

```bash
# Start Streamlit dashboard
streamlit run src/dashboard.py
```

Visit http://localhost:8501 to view analytics.

## What You'll See

- DAU (Daily Active Users)
- Revenue and ARPU metrics
- Retention curves (D1, D7, D30)
- Session and engagement metrics
- Level completion rates

## Next Steps

After running these commands, you'll have a fully functional analytics pipeline demonstrating:
- Event generation with realistic player behavior
- ETL processing with Polars for performance
- Interactive dashboard with business metrics
