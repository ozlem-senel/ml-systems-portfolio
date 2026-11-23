# Level Progression & Difficulty Analysis

A descriptive analysis of synthetic game telemetry generated and cleaned by project 03. Each level attempt has an ID joining its start and outcome. Level 12, 25 and 40 have simulated difficulty spikes; these are test scenarios, not findings about a real game.

## Run

From the repository root:

```bash
cd 03-event-analytics-pipeline
python src/event_generator.py --players 1000 --days 30
python src/etl_pipeline.py --input data/raw_events/events_YYYYMMDD.jsonl
cd ../05-level-progression-analysis
python src/analysis.py --input ../03-event-analytics-pipeline/data/processed/events_cleaned.parquet
```

Replace the input filename with the one printed by the generator. Run the Streamlit dashboard from project 03 to see the level charts. Previously generated events do not have attempt IDs; generate fresh data first.

## Definitions and limits

- Completion is the share of starters who completed a level within the observed dataset; recent starters may not have had enough time to complete it.
- Reach rate is the share of players with any recorded level start who started the level.
- First-attempt win rate is the share of starters whose first recorded attempt has a completion event. Incomplete or ambiguous outcomes are not wins.
- First-win confidence limits use a 95% Wilson interval; this quantifies sampling uncertainty, not selection bias.
- Median attempts counts recorded starts per player, including players who have not completed.
- Seven-day level abandonment is the share of players whose last level attempt was at least seven days before the dataset's final event and who have not completed that level. It is not game churn. Players without a full seven-day window are excluded from its denominator.
- Missing or conflicting outcomes remain incomplete. Duplicate starts for an attempt ID are excluded. The data is synthetic and observational; rates and associations do not establish causal effects.
