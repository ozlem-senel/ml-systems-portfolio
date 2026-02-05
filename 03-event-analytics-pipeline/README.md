# Game Event Analytics Pipeline

ETL pipeline for processing game event streams and generating product metrics.

## Objectives

- Simulate realistic game event telemetry
- Build ETL pipeline: ingest, clean, aggregate, analyze
- Generate key product metrics: DAU, session length, conversion funnels
- Visualize metrics in an analytics dashboard

## Business Context

Player actions generate events like login, level_complete, purchase, and ad_watched. This project demonstrates processing high-volume event data efficiently to derive actionable product metrics for data-driven decisions.

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

**Setup:**
```bash
cd 03-event-analytics-pipeline

# Install dependencies
pip install -r requirements.txt

# Generate events
python src/event_generator.py --days 30 --users 5000

# Run ETL pipeline
python src/etl_pipeline.py

# Launch dashboard
streamlit run src/dashboard.py
```

**Expected output:**
- Event data: 500K+ events over 30 days
- Processed metrics: daily aggregations by cohort and event type
- Dashboard visualizations

## Event Types

**Player Events:**
- session_start, session_end: Track engagement
- level_start, level_complete: Progression
- purchase, ad_watched: Monetization
- achievement_unlocked: Engagement milestones

**Event Schema:**
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

**1. Ingestion**
- Read raw event logs (JSON or CSV)
- Validate schema and handle malformed records

**2. Cleaning & Enrichment**
- Remove duplicates
- Parse timestamps
- Enrich with player metadata (cohort, acquisition date)

**3. Aggregation**
- Calculate metrics by day, cohort, event type
- Build conversion funnels
- Session aggregation: session length, events per session

**4. Storage**
- Save to Parquet or DuckDB for fast analytics

**5. Visualization**
- Streamlit dashboard with key metrics

## Key Metrics

**Engagement:**
- DAU (Daily Active Users): Unique players per day
- Session length: Average time per session
- Retention: D1, D7, D30 retention rates

**Monetization:**
- ARPU (Average Revenue Per User): Total revenue divided by total users
- Conversion rate: Percentage of players making IAP
- Ad revenue: Total from ad impressions

**Product:**
- Level completion rates: Funnel analysis
- Feature adoption: Percentage using new features

## Technology Choices

**Polars vs Pandas:**
- Polars: Faster for large datasets with lazy evaluation
- Pandas: More familiar, good for prototyping

**DuckDB:**
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

---

Status: In Progress | Last Updated: Feb 2026
