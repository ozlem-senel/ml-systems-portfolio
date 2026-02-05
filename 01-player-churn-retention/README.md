# Player Churn & Retention System

Predict player churn and analyze retention patterns using simulated mobile game telemetry data.

## Objectives

- Build a churn prediction model for mobile game players
- Analyze retention curves and cohort behavior
- Generate actionable insights for player engagement strategies
- Create an interactive dashboard for stakeholder review

## Business Context

Player retention directly impacts revenue in mobile gaming. This project addresses:
- Problem: Players churning within first 7-30 days
- Solution: Predictive model to identify at-risk players for re-engagement
- Impact: Improved retention leading to higher lifetime value

## Project Structure

```
01-player-churn-retention/
├── data/                   # Generated datasets
│   ├── raw/               # Simulated player telemetry
│   └── processed/         # Cleaned and engineered features
├── notebooks/             # Exploratory analysis
│   ├── 01_data_generation.ipynb
│   ├── 02_eda.ipynb
│   └── 03_modeling.ipynb
├── src/                   # Source code
│   ├── data_generator.py  # Generate synthetic game data
│   ├── features.py        # Feature engineering
│   ├── models.py          # Model training and evaluation
│   └── dashboard.py       # Streamlit dashboard
├── models/                # Saved model artifacts
├── reports/               # Analysis outputs
│   └── figures/          # Plots and visualizations
├── requirements.txt       # Project-specific dependencies
└── README.md
```

## Quick Start

**Setup:**
```bash
cd 01-player-churn-retention

# Install dependencies
pip install -r requirements.txt

# Generate synthetic data
python src/data_generator.py

# Train model
python src/models.py

# Launch dashboard
streamlit run src/dashboard.py
```

**Expected output:**
- Churn prediction model saved in `models/`
- Feature importance analysis
- Retention curves by cohort
- Streamlit dashboard at `http://localhost:8501`

## Features

**Data features:**
- Player demographics: acquisition source, device type, country
- Engagement metrics: session count, playtime, days active
- Monetization: IAP purchases, ad interactions
- Progression: levels completed, achievements

**Model:**
- Algorithm: XGBoost or Random Forest
- Target: Binary churn (active vs churned within 30 days)
- Evaluation: ROC-AUC, Precision-Recall, Feature Importance

**Dashboard components:**
1. KPI overview: DAU, retention rate, churn rate
2. Retention curves: D1, D7, D30
3. Cohort analysis
4. High-risk player segments
5. Feature impact visualization

## Methodology

1. Data Generation: Simulate 10,000+ players with realistic behavior patterns
2. Feature Engineering: Time-based aggregations and engagement ratios
3. Model Training: Train/validation/test split with hyperparameter tuning
4. Evaluation: Business-focused metrics (identifying 80% of churners in top 20% risk scores)
5. Dashboard: Streamlit interface for stakeholder review

## Example Insights

- Players with fewer than 5 sessions in first week have 75% churn rate
- IAP users show 3x retention compared to non-payers
- Evening players demonstrate 20% higher retention than morning players

## Integration

- Generates sample data for Project 3 (Event Pipeline)
- Model tracked by Project 4 (ML Experiment API)

## Skills Demonstrated

- Binary classification
- Feature engineering for time-series behavior
- Business metric interpretation: DAU, retention, LTV
- Data visualization
- Product-oriented analysis

---

Status: In Progress | Last Updated: Feb 2026
