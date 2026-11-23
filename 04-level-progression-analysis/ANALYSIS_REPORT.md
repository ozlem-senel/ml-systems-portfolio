# Level progression analysis — synthetic sample

Generated from `events_cleaned.parquet`. This is one simulation, not real player data.
The date range is 2026-09-14 00:01:00 to 2026-11-22 23:48:28; it contains 1,200 observed players and 373,656 events.

## Progression

Level 12: 967 started, 954 completed, and 932 started level 13 after completing level 12, through the observation cutoff. These stages are not fixed-duration conversion rates; later starters have had less time.

## Difficulty and prioritization

Rank uses the positive first-attempt win-rate gap to levels within ±2 (minimum 30 players per level), multiplied by the number of starters. It is a heuristic, not a causal impact estimate. Neighboring levels can have overlapping confidence intervals and different player populations.

| Level | Starters | First-attempt win | Neighbor rate | Gap |
|---|---:|---:|---:|---:|
| 12 | 967 | 54.2% | 77.8% | 23.6% |
| 25 | 783 | 48.7% | 76.1% | 27.5% |
| 40 | 689 | 50.4% | 76.2% | 25.9% |
| 43 | 673 | 72.1% | 76.2% | 4.1% |
| 81 | 436 | 68.6% | 73.5% | 4.9% |

## Retry and abandonment

For level 12, 403 of 413 players with a first failure observed at least seven days before cutoff retried within seven days (97.6%). The seven-day level abandonment measure is 0.6% among 886 players with a mature last attempt. These measures use different populations; abandonment is not game churn.

## Simulation check

The generator injects difficulty spikes at levels 12, 25 and 40. Of these, 3/3 occur in the top 10 ranked levels: 12, 25, 40. This is an in-sample check against the same generator used to design the heuristic, not independent validation or evidence about real players.

## Proposed experiment — level 12

Hypothesis: an explanatory hint at the first obstacle can improve level 12 completion. Randomize eligible players at their first level 12 start to existing experience or hint, keeping other rules unchanged. Primary metric: proportion completing level 12 within 24 hours of first start. Secondary: first-attempt win rate and seven-day retention; guardrails: later-level progression and session duration. Define exposure, observation windows, sample size and minimum detectable effect before launch; analyze at player level. This is a proposed experiment, not a result.
