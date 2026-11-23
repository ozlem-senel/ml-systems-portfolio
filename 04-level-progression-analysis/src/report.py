"""Generate a reproducible synthetic-data report and site figures."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import pandas as pd
from analysis import level_metrics, prioritize_levels


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--figures', type=Path, default=Path('../portfolio-site/public/projects/level-progression'))
    parser.add_argument('--report', type=Path, default=Path('ANALYSIS_REPORT.md'))
    args = parser.parse_args()
    events = pd.read_parquet(args.input)
    metrics = level_metrics(events)
    ranked = prioritize_levels(metrics, min_players=30)
    known = {12, 25, 40}
    top10 = set(ranked.head(10).level)
    flagged = known & top10
    args.figures.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False})
    curve = metrics[metrics.level.between(1, 50)]
    fig, ax = plt.subplots(figsize=(10, 4.2), layout='constrained')
    ax.plot(curve.level, curve.first_attempt_win_rate, color='#2563eb', linewidth=2)
    spikes = curve[curve.level.isin(known)]
    ax.scatter(spikes.level, spikes.first_attempt_win_rate, color='#dc6b32', s=50, zorder=3)
    for _, row in spikes.iterrows(): ax.annotate(f"Level {int(row.level)}", (row.level, row.first_attempt_win_rate), xytext=(0,-25), textcoords='offset points', ha='center')
    ax.yaxis.set_major_formatter(PercentFormatter(1)); ax.set_ylim(0, 1); ax.set(xlabel='Level', ylabel='First-attempt win rate', title='Difficulty curve · simulated players')
    ax.grid(axis='y', alpha=.2); fig.savefig(args.figures / 'difficulty-curve.png', dpi=150); plt.close(fig)
    row = metrics[metrics.level == 12].iloc[0]
    fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
    labels = ['Started level 12', 'Completed level 12', 'Started level 13']
    values = [int(row.players_started), int(row.players_completed), int(row.next_level_players)]
    bars = ax.barh(labels[::-1], values[::-1], color=['#a78bfa', '#60a5fa', '#2563eb'])
    ax.bar_label(bars, padding=5); ax.set_xlim(0, max(values)*1.18); ax.set(xlabel='Players', title='Progression funnel · level 12'); ax.grid(axis='x', alpha=.15)
    fig.savefig(args.figures / 'level-12-funnel.png', dpi=150); plt.close(fig)
    subset = metrics[metrics.level.isin(known)].sort_values('level')
    fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
    bars = ax.bar([str(int(x)) for x in subset.level], subset.retry_rate_7d, color='#7c3aed', width=.5)
    for bar, (_, r) in zip(bars, subset.iterrows()):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+.025, f"{r.retry_rate_7d:.0%}\n(n={int(r.retry_eligible)})", ha='center', va='bottom')
    ax.yaxis.set_major_formatter(PercentFormatter(1)); ax.set_ylim(0,1.18); ax.set(xlabel='Level', ylabel='Players with a mature first failure', title='Retried within 7 days · simulated players')
    ax.grid(axis='y', alpha=.15); fig.savefig(args.figures / 'retry-rate.png', dpi=150); plt.close(fig)
    rows = []
    for _, r in ranked.head(5).iterrows():
        rows.append(f"| {int(r.level)} | {int(r.players_started)} | {r.first_attempt_win_rate:.1%} | {r.neighbor_win_rate:.1%} | {r.gap:.1%} |")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(f'''# Level progression analysis — synthetic sample

Generated from `{args.input.name}`. This is one simulation, not real player data.
The date range is {events.timestamp.min()} to {events.timestamp.max()}; it contains {events.player_id.nunique():,} observed players and {len(events):,} events.

## Progression

Level 12: {values[0]:,} started, {values[1]:,} completed, and {values[2]:,} started level 13 after completing level 12, through the observation cutoff. These stages are not fixed-duration conversion rates; later starters have had less time.

## Difficulty and prioritization

Rank uses the positive first-attempt win-rate gap to levels within ±2 (minimum 30 players per level), multiplied by the number of starters. It is a heuristic, not a causal impact estimate. Neighboring levels can have overlapping confidence intervals and different player populations.

| Level | Starters | First-attempt win | Neighbor rate | Gap |
|---|---:|---:|---:|---:|
''' + '\n'.join(rows) + f'''

## Retry and abandonment

For level 12, {int(row.retried_7d)} of {int(row.retry_eligible)} players with a first failure observed at least seven days before cutoff retried within seven days ({row.retry_rate_7d:.1%}). The seven-day level abandonment measure is {row.abandonment_rate:.1%} among {int(row.mature_players)} players with a mature last attempt. These measures use different populations; abandonment is not game churn.

## Simulation check

The generator injects difficulty spikes at levels 12, 25 and 40. Of these, {len(flagged)}/3 occur in the top 10 ranked levels: {', '.join(map(str, sorted(flagged))) or 'none'}. This is an in-sample check against the same generator used to design the heuristic, not independent validation or evidence about real players.

## Proposed experiment — level 12

Hypothesis: an explanatory hint at the first obstacle can improve level 12 completion. Randomize eligible players at their first level 12 start to existing experience or hint, keeping other rules unchanged. Primary metric: proportion completing level 12 within 24 hours of first start. Secondary: first-attempt win rate and seven-day retention; guardrails: later-level progression and session duration. Define exposure, observation windows, sample size and minimum detectable effect before launch; analyze at player level. This is a proposed experiment, not a result.
''')
    print(f'Saved report to {args.report}; detected {len(flagged)}/3 synthetic spikes in top 10.')


if __name__ == '__main__':
    main()
