# ML Systems Portfolio

End-to-end machine learning and data engineering projects showcasing production-ready systems for gaming analytics. Each project demonstrates practical skills from data processing through deployment.

## About

This portfolio demonstrates my ability to build complete ML systems, from data generation and feature engineering to model deployment and production monitoring.

## Completed Projects

### 1. Player Churn & Retention System

Complete with 3 production models and A/B testing framework

Comprehensive churn prediction system with traditional ML and deep learning approaches, plus experimental framework for retention interventions.

What I built:
- Realistic player behavior data generator (10K players, 135K observations, 63.6% churn rate)
- 31 engineered features: aggregations, recency metrics, behavioral trends
- 3 trained models: XGBoost (0.773 AUC), LSTM (0.780 AUC), GRU (0.780 AUC)
- A/B testing simulator: 6 interventions tested with statistical significance
- Model comparison framework with ROC/PR curves and business impact analysis

Key results:
- GRU model selected as best: 0.780 AUC with 24% fewer parameters than LSTM
- Tutorial improvement intervention: 22.8% churn reduction (p < 0.001)
- Comprehensive documentation: AB_TESTING_SUMMARY.md with implementation priorities

Skills demonstrated: PyTorch, XGBoost, Feature Engineering, Statistical Testing, Model Comparison  
Stack: Python, PyTorch, XGBoost, scikit-learn, Polars, Matplotlib

[View Project](01-player-churn-retention/) | [View Results](01-player-churn-retention/AB_TESTING_SUMMARY.md)

---

### 3. Game Event Analytics Pipeline

Production-ready with comprehensive monitoring and testing

High-performance ETL pipeline processing 940K events with production-grade error handling, data quality checks, and monitoring.

What I built:
- Event data generator: 5K players, 30 days, 8 event types, 5 player segments
- Production ETL pipeline: 112K events/sec throughput (Polars-based)
- Data quality framework: 6 validation checks with configurable thresholds
- Interactive Streamlit dashboard: DAU, revenue, retention metrics
- Unit tests: 4 passing tests covering core functionality
- Comprehensive YAML configuration system

Technical highlights:
- Processes 940K events in 8.4 seconds
- Comprehensive logging (file + console)
- Custom exception handling and error recovery
- Metrics tracking: throughput, processing time, failed events
- Documentation: PRODUCTION.md with deployment guide and troubleshooting

Skills demonstrated: Data Engineering, ETL, Polars, Production Systems, Testing  
Stack: Python, Polars, DuckDB, Streamlit, Plotly, PyYAML, pytest

[View Project](03-event-analytics-pipeline/) | [Production Guide](03-event-analytics-pipeline/PRODUCTION.md)

---

### 2. Support Ticket RAG System

Complete with working API and multiple LLM support

AI-powered support ticket processing using Retrieval-Augmented Generation with semantic search and LLM integration.

What I built:
- 500 synthetic support tickets across 4 categories
- 15 curated knowledge base documents
- Vector embeddings with sentence-transformers
- RAG pipeline with Mock, OpenAI, and Gemini LLM options
- FastAPI endpoint for ticket processing
- Real-time AI response generation

Key results:
- Processes tickets in <1 second
- 0.619-0.785 similarity scores for document retrieval
- 100% classification accuracy on test cases
- Working with free Gemini API (1500 requests/day)

Skills demonstrated: RAG, LLMs, Semantic Search, FastAPI, Vector Embeddings  
Stack: Python, sentence-transformers, FastAPI, Google Gemini, scikit-learn

[View Project](02-support-ticket-rag/) | [View Results](02-support-ticket-rag/PROJECT_COMPLETE.md)

---

### 4. ML Experiment Tracking & Model API

Status: Planned

Experiment tracking and model serving infrastructure with containerization.

Skills: MLOps, API design, Docker, experiment logging  
Stack: FastAPI, MLflow, Docker

[`04-ml-experiment-api/`](04-ml-experiment-api/)

## Repository Structure

```
ml-systems-portfolio/
├── 01-player-churn-retention/      # Churn prediction with ML/DL + A/B testing
│   ├── src/                        # Data generation, models, A/B testing
│   ├── models/                     # Trained models (XGBoost, LSTM, GRU)
│   ├── output/                     # Visualizations and results
│   └── AB_TESTING_SUMMARY.md       # Comprehensive analysis report
├── 02-support-ticket-rag/          # RAG system with LLM integration
│   ├── src/                        # RAG pipeline, embeddings, API
│   ├── data/                       # Tickets, knowledge base, results
│   ├── vector_store/               # Embeddings and search index
│   └── PROJECT_COMPLETE.md         # Implementation summary
├── 03-event-analytics-pipeline/    # Production ETL with monitoring
│   ├── src/                        # Event generator, ETL, dashboard
│   ├── config/                     # YAML configuration
│   ├── tests/                      # Unit tests
│   ├── logs/                       # Pipeline logs
│   └── PRODUCTION.md               # Deployment guide
├── 04-ml-experiment-api/           # Planned
└── README.md
```

## Technical Skills Demonstrated

Machine learning:
- Binary classification (churn prediction)
- Deep learning with PyTorch (LSTM, GRU architectures)
- Gradient boosting (XGBoost)
- Feature engineering (31 features from behavioral data)
- Model comparison and selection
- Retrieval-Augmented Generation (RAG)
- Semantic search with vector embeddings
- LLM integration and prompt engineering

Data engineering:
- High-performance ETL with Polars (112K events/sec)
- Data quality validation framework
- Production error handling and logging
- YAML-based configuration management
- Parquet file optimization

Software engineering:
- Unit testing with pytest
- Production-ready code structure
- Comprehensive documentation
- Version control best practices
- Error recovery and monitoring

Statistical analysis:
- A/B testing with chi-squared tests
- Wilson confidence intervals
- Statistical power analysis
- Sample size calculations
- Business impact quantification

Tools and technologies:
- Languages: Python 3.9+
- ML: PyTorch, XGBoost, scikit-learn, sentence-transformers
- LLMs: Google Gemini, OpenAI GPT
- Data: Polars, Pandas, DuckDB
- APIs: FastAPI, uvicorn
- Visualization: Matplotlib, Seaborn, Plotly, Streamlit
- Testing: pytest
- Config: YAML, logging

## Setup & Installation

Prerequisites:
- Python 3.9+
- 8GB+ RAM recommended
- 2GB free disk space

Quick start:
```bash
# Clone the repository
git clone https://github.com/ozlem-senel/ml-systems-portfolio.git
cd ml-systems-portfolio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (per project)
cd 01-player-churn-retention
pip install -r requirements.txt
```

Running projects:
See individual project READMEs for detailed instructions:
- [Project 1: Churn Prediction](01-player-churn-retention/README.md)
- [Project 2: Support Ticket RAG](02-support-ticket-rag/README.md)
- [Project 3: Event Analytics](03-event-analytics-pipeline/README.md)


## Contact & Links

Portfolio Site: Coming soon (Next.js showcase)  
GitHub: github.com/ozlem-senel  
LinkedIn: linkedin.com/in/ozlem-senel

---

Last updated: February 14, 2026  
Projects: 3 of 4 completed