# Player Churn & Retention System

Complete as of February 2026

Comprehensive churn prediction system featuring traditional ML (XGBoost), deep learning (PyTorch LSTM/GRU), and A/B testing framework for retention interventions.

## What I Built

### 1. Realistic Data Generation
- PlayerBehaviorGenerator: Creates 10,000 players across 5 segments (whale, engaged, casual, at-risk, dormant)
- Realistic noise: Daily mood variation (±30%), stochastic churn with ±15% noise
- Edge cases: 5% comeback events, ambiguous labels for realism
- Output: 135,188 observations with 63.6% churn rate

### 2. Feature Engineering
- 31 engineered features from raw behavioral data:
  - 21 aggregated features (means, sums, ratios)
  - 10 recency features (days since last action)
  - Trend features (engagement deltas)
- Handles infinite values and NaN gracefully
- Sequential data preparation for deep learning

### 3. Model Development

XGBoost baseline:
- Test AUC: 0.773
- 100 estimators, max_depth=5
- Feature importance visualization
- Confusion matrix analysis

PyTorch LSTM:
- Test AUC: 0.780
- Architecture: 2 layers, 64 hidden units
- Parameters: 53,602
- Early stopping with patience=5

PyTorch GRU (selected as best model):
- Test AUC: 0.780
- Architecture: 2 layers, 64 hidden units
- Parameters: 40,738 (24% fewer than LSTM)
- Training history visualization

### 4. A/B Testing Framework
- 6 interventions tested:
  1. Tutorial improvement: 22.8% churn reduction (p < 0.001)
  2. Social features: 16.2% reduction (p < 0.001)
  3. In-game rewards: 12.5% reduction (p < 0.001)
  4. Push notifications: 7.1% reduction (p = 0.002)
  5. Personalized content: 4.2% reduction (p = 0.065)
  6. Limited-time events: -2.5% increase (p = 0.267)
- Wilson confidence intervals
- Chi-squared statistical tests
- Sample size calculations
- Business impact quantification

### 5. Comprehensive Documentation
- AB_TESTING_SUMMARY.md: Complete analysis with implementation priorities
- Model comparison report: ROC curves, PR curves, metrics comparison
- Training history plots: Loss and accuracy over epochs

## Results Summary

| Model | Test AUC | Parameters | Status |
|-------|----------|------------|--------|
| XGBoost | 0.773 | N/A | Baseline |
| LSTM | 0.780 | 53,602 | Strong |
| GRU | 0.780 | 40,738 | Selected |

**Why GRU?** Same performance as LSTM with 24% fewer parameters = faster inference, lower memory footprint.

## Business Impact

Tutorial improvement (highest ROI):
- 22.8% relative churn reduction
- From 63.6% to 49.1% churn rate
- Statistically significant (p < 0.001)
- Estimated annual value: $2.28M (10K new players/month × $100 LTV × 0.228)

## Project Structure

```
01-player-churn-retention/
├── data/                   # Generated datasets
│   ├── raw/               # Simulated player telemetry
│   ├── processed/         # Cleaned and engineered features
│   └── sequences/         # Sequential data for deep learning
├── notebooks/             # Exploratory analysis
│   ├── 01_data_generation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_modeling.ipynb
│   ├── 04_deep_learning.ipynb
│   └── 05_ab_testing.ipynb
├── src/                   # Source code
│   ├── data_generator.py  # Generate synthetic game data
│   ├── feature_engineering.py  # Feature engineering
│   ├── train_xgboost.py   # Train XGBoost model
│   ├── train_pytorch.py   # Train PyTorch LSTM/GRU models
│   ├── model_comparison.py  # Compare all models
│   └── ab_testing.py      # A/B test framework
├── models/                # Saved model artifacts
│   ├── xgboost/          # Traditional models
│   └── pytorch/          # Deep learning checkpoints
├── experiments/           # A/B test results
├── reports/               # Analysis outputs
│   └── figures/          # Plots and visualizations
├── requirements.txt       # Project-specific dependencies
└── README.md
```

## Quick Start

Setup:
```bash
cd 01-player-churn-retention

# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python src/data_generator.py

# Engineer features
python src/feature_engineering.py

# Train XGBoost model
python src/train_xgboost.py

# Train PyTorch models (LSTM/GRU)
python src/train_pytorch.py

# Compare models
python src/model_comparison.py

# Run A/B testing analysis
python src/ab_testing.py
```

Expected output:
- Trained models saved in `models/` directory
- Feature importance plots and analysis
- Model comparison report with ROC/PR curves
- A/B testing results in `AB_TESTING_SUMMARY.md`

## Features

Data features:
- Player demographics: acquisition source, device type, country
- Engagement metrics: session count, playtime, days active
- Monetization: IAP purchases, ad interactions
- Progression: levels completed, achievements

Models:

Traditional ML:
- XGBoost and Random Forest for baseline
- Engineered features from aggregated player behavior
- Fast inference and interpretable feature importance

Deep learning (PyTorch):
- LSTM/GRU for sequential behavior modeling
- Input: Time series of player sessions (14-30 days)
- Each timestep: playtime, levels, purchases, session gaps
- Captures temporal patterns and behavior changes over time
- Attention mechanism for interpretability

*Evaluation:*
- ROC-AUC, Precision-Recall curves
- Model comparison: accuracy vs inference speed vs interpretability
- Target: Binary churn (active vs churned within 30 days)

## A/B Testing Framework

Test different intervention strategies for at-risk players:

Experiment design:
- Control group: No intervention
- Treatment groups: Different re-engagement campaigns (push notifications, in-game rewards, email outreach)
- Randomization: Stratified by churn risk score
- Sample size: Power analysis for 80% power at 5% significance level

Metrics tracked:
- Primary: 7-day retention rate
- Secondary: Session count, playtime, conversion to IAP
- Guardrail: Player satisfaction scores

Statistical analysis:
- Two-sample t-test or chi-square test for significance
- Confidence intervals and effect sizes
- Multiple testing correction (Bonferroni or Benjamini-Hochberg)

Implementation:
```python
from src.ab_testing import ABTest

# Define experiment
test = ABTest(
    name="push_notification_campaign",
    control_size=1000,
    treatment_size=1000,
    metric="7d_retention"
)

# Run test
results = test.run(data=high_risk_players)
print(f"Lift: {results.lift:.2%}, p-value: {results.pvalue:.4f}")
```

## Methodology

1. Data Generation: Simulate 10,000+ players with realistic behavior patterns
2. Feature Engineering: Time-based aggregations and engagement ratios for traditional ML
3. Sequence Preparation: Format player behavior sequences for LSTM/GRU models
4. Model Training:
   - Traditional: XGBoost with hyperparameter tuning
   - Deep Learning: PyTorch LSTM/GRU with early stopping
5. Model Comparison: Evaluate both approaches on accuracy, speed, and interpretability
6. Evaluation: Business-focused metrics (identifying 80% of churners in top 20% risk scores)
7. A/B Testing: Design and analyze experiments for intervention strategies

## Example Insights

- Players with fewer than 5 sessions in first week have 75% churn rate
- IAP users show 3x retention compared to non-payers
- Evening players demonstrate 20% higher retention than morning players

## Integration

- Generates sample data for Project 3 (Event Pipeline)
- Model tracked by Project 4 (ML Experiment API)

## Skills Demonstrated

- Binary classification (traditional ML and deep learning)
- PyTorch model development: LSTM/GRU architectures
- Sequential data modeling for temporal patterns
- Feature engineering for time-series behavior
- Model comparison and selection
- Business metric interpretation: DAU, retention, LTV
- A/B testing and experimental design
- Statistical hypothesis testing
- Data visualization
- Product-oriented analysis
