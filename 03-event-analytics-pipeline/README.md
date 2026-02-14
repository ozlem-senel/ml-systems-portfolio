# Game Event Analytics Pipeline

High-performance ETL pipeline for processing game event streams with production-grade monitoring, error handling, and data quality validation.

## What I Built

### 1. Event Data Generator
- 5,000 players across 5 behavioral segments
- 30 days of realistic event data
- 8 event types: session_start, session_end, level_start, level_complete, purchase, ad_watched, achievement_unlocked
- Monetization modeling: 8% payer rate, 25% purchase probability
- Output: 940,324 events (934,881 processed successfully)

### 2. Production ETL Pipeline (`etl_pipeline_prod.py`)

Performance:
- Processes 940K events in 8.4 seconds
- Throughput: 112,000 events/second
- Memory efficient with Polars lazy evaluation

Data quality framework:
- Minimum event count validation (1,000 threshold)
- Required event type verification (session_start, session_end)
- Null percentage monitoring (10% threshold)
- Duplicate event detection
- Future timestamp detection (1 day threshold)
- Outlier detection (max revenue $1,000)

Error handling:
- Custom `DataQualityError` exception class
- Graceful handling of malformed JSON lines
- Maximum failure threshold (100 failed lines)
- Comprehensive error logging with stack traces

Monitoring and metrics:
- Events loaded/cleaned/failed counters
- Processing time tracking
- Throughput calculation (events/sec)
- Quality check summaries
- Dual logging (file + console)

### 3. Configuration Management
- YAML-based config (`config/etl_config.yaml`)
- Externalized quality check thresholds
- Configurable strict mode (warnings vs. errors)
- Environment-specific settings support
- Fallback to sensible defaults

### 4. Interactive Dashboard
- Streamlit web app with date range filtering
- KPI metrics: DAU, Total Events, ARPU, Retention Rate
- Time-series visualizations:
  - Daily Active Users trend
  - Total Events by type
  - Revenue per Day
  - Retention cohort curves
- Real-time data refresh
- Responsive design

### 5. Testing & Documentation

Unit tests (`tests/test_etl_pipeline.py`):
- 4 passing tests covering:
  - Event loading and parsing
  - Input file validation
  - Error handling for missing files
  - Data quality check framework
- pytest framework with fixtures
- Test coverage for core functionality

Production guide (`PRODUCTION.md`):
- Comprehensive deployment checklist
- Configuration reference
- Troubleshooting guide with common issues
- Performance benchmarks
- Security best practices
- Monitoring strategies

## Technical Highlights

### Architecture
```
Raw Events (JSONL) → Load & Validate → Clean & Enrich → Aggregate → Output (Parquet)
                           ↓                ↓               ↓
                    Quality Checks    Add Features    Metrics Calc
                    Error Handling      Logging      Retention Cohorts
```

### Data Flow
1. **Input**: JSONL files with event data
2. **Validation**: File size, schema, required fields
3. **Loading**: Streaming read with error recovery
4. **Quality Checks**: 6 validations with configurable thresholds
5. **Transformation**: Property flattening, datetime parsing, enrichment
6. **Aggregation**: Daily metrics (DAU, revenue, events), retention cohorts
7. **Output**: 3 Parquet files (events_cleaned, daily_metrics, retention_cohorts)

### Key Metrics Generated
- Daily Active Users (DAU)
- Total Events by Type
- Revenue per Day
- Average Revenue Per User (ARPU)
- Retention Rate (Day 1, Day 7, Day 30)
- Cohort Retention Curves

## Project Structure

```
03-event-analytics-pipeline/
├── data/
│   ├── raw_events/           # Simulated event logs
│   └── processed/            # Aggregated metrics
├── notebooks/
│   ├── 01_event_generation.ipynb
│   ├── 02_etl_prototype.ipynb
│   └── 03_analytics.ipynb
├── src/
│   ├── event_generator.py    # Generate synthetic events
│   ├── etl_pipeline.py       # Data processing
│   ├── metrics.py            # Metric calculations
│   └── dashboard.py          # Streamlit dashboard
├── sql/                      # SQL queries (if using DuckDB)
├── tests/
├── requirements.txt
└── README.md
```

## Quick Start

Setup:
```bash
cd 03-event-analytics-pipeline

# Install dependencies
pip install -r requirements.txt

# Generate events
python src/event_generator.py --days 30 --players 5000

# Run ETL pipeline (specify the generated file)
python src/etl_pipeline.py --input data/raw_events/events_20260112.jsonl

# Launch dashboard
streamlit run src/dashboard.py
```

Expected output:
- Event data: 500K+ events over 30 days
- Processed metrics: daily aggregations by cohort and event type
- Dashboard visualizations

## Event Types

Player events:
- session_start, session_end: Track engagement
- level_start, level_complete: Progression
- purchase, ad_watched: Monetization
- achievement_unlocked: Engagement milestones

Event schema:
```json
{
  "event_id": "uuid",
  "player_id": "uuid",
  "event_type": "level_complete",
  "timestamp": "2026-02-05T14:32:00Z",
  "properties": {
    "level": 5,
    "time_spent": 120,
    "success": true
  }
}
```

## Pipeline Stages

1. Ingestion
- Read raw event logs (JSON or CSV)
- Validate schema and handle malformed records

2. Cleaning & Enrichment
- Remove duplicates
- Parse timestamps
- Enrich with player metadata (cohort, acquisition date)

3. Aggregation
- Calculate metrics by day, cohort, event type
- Build conversion funnels
- Session aggregation: session length, events per session

4. Storage
- Save to Parquet or DuckDB for fast analytics

5. Visualization
- Streamlit dashboard with key metrics

## Key Metrics

Engagement:
- DAU (Daily Active Users): Unique players per day
- Session length: Average time per session
- Retention: D1, D7, D30 retention rates

Monetization:
- ARPU (Average Revenue Per User): Total revenue divided by total users
- Conversion rate: Percentage of players making IAP
- Ad revenue: Total from ad impressions

Product:
- Level completion rates: Funnel analysis
- Feature adoption: Percentage using new features

## Technology Choices

Polars vs Pandas:
- Polars: Faster for large datasets with lazy evaluation
- Pandas: More familiar, good for prototyping

DuckDB:
- Embedded SQL database for analytics on local datasets
- 10-100x faster than Pandas for aggregations

## Integration

- Generates telemetry data for Project 1 (Churn Model)
- Could stream events in real-time with future Kafka integration

## Skills Demonstrated

- ETL pipeline design
- Event-driven data modeling
- Efficient data processing with Polars and DuckDB
- Product analytics
- Data visualization

## Future Work

- Real-time streaming with Kafka
- Time-series forecasting (predict tomorrow's DAU)
- Anomaly detection for unusual player behavior
- A/B test analysis module
