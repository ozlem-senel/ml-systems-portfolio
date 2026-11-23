# Level Progression & Difficulty Analysis

A descriptive analysis of synthetic game telemetry generated and cleaned by project 03. Each level attempt has an ID joining its start and outcome. Level 12, 25 and 40 have simulated difficulty spikes; these are test scenarios, not findings about a real game.

## Run

From the repository root:

```bash
cd 03-event-analytics-pipeline
python src/event_generator.py --players 1000 --days 30
python src/etl_pipeline.py --input data/raw_events/events_YYYYMMDD.jsonl
cd ../04-level-progression-analysis
python src/analysis.py --input ../03-event-analytics-pipeline/data/processed/events_cleaned.parquet
```

Replace the input filename with the one printed by the generator. Run the Streamlit dashboard from project 03 to see the level charts. Previously generated events do not have attempt IDs; generate fresh data first.

## Definitions and limits

- Completion is the share of starters who completed a level within the observed dataset; recent starters may not have had enough time to complete it.
- Reach rate is the share of players with any recorded level start who started the level.
- First-attempt win rate is the share of starters whose first recorded attempt has a completion event. Incomplete or ambiguous outcomes are not wins.
- First-win confidence limits use a 95% Wilson interval; this quantifies sampling uncertainty, not selection bias.
- Mean and median attempts count recorded starts per player, including players who have not completed. The dashboard uses the mean because the median is often one and hides retry differences.
- Dashboard date filtering selects player-levels whose first recorded start falls in the selected dates. Outcomes and retries are observed only through the end date; earlier activity is retained to identify genuine first starts. Recent cohorts may have less time to complete.
- Seven-day level abandonment is the share of players whose last level attempt was at least seven days before the dataset's final event and who have not completed that level. It is not game churn. Players without a full seven-day window are excluded from its denominator.
- Missing or conflicting outcomes remain incomplete. Duplicate starts for an attempt ID are excluded. The data is synthetic and observational; rates and associations do not establish causal effects.

## Funnel, difficulty and report

The dashboard includes a range-based progression funnel following the same players through consecutive level starts, retry within seven days after the first failure, and a ranked list of levels whose first-attempt win rates fall below nearby levels. Ranking uses the gap to levels within ±2 multiplied by starters, with a minimum sample threshold; it is a prioritization heuristic, not a causal effect or a significance test. The range funnel selects players whose first start of the starting level falls within the chosen dates, and follows consecutive starts through the selected end date. Recent starters have less time to progress. The static report separately shows a single-level completion funnel.

A player is eligible for the retry metric when their first recorded failure has a full seven-day follow-up before the data cutoff. Retry and abandonment have different denominators. Confidence intervals and player counts remain available in the detail table.

Reproduce the example analysis and site figures from the repository root:

```bash
python 04-level-progression-analysis/src/report.py \
  --input 03-event-analytics-pipeline/data/processed/events_cleaned.parquet \
  --figures portfolio-site/public/projects/level-progression \
  --report 04-level-progression-analysis/ANALYSIS_REPORT.md
```

See [ANALYSIS_REPORT.md](ANALYSIS_REPORT.md) for the specific sample, simulation sanity check, limitations and proposed A/B experiment. Recompute both the figures and the portfolio page's quoted numbers if the source data changes. The sample-specific simulation check is not independent validation.
