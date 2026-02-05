# ML Systems Portfolio

End-to-end machine learning projects focused on gaming analytics, LLM applications, and production systems. Each project demonstrates practical skills from data processing through deployment.

## Overview

This repository contains four interconnected projects relevant to data science and ML engineering roles:

**Target applications:**
- Data Science/AI roles in mobile gaming (player analytics, retention modeling, product insights)
- ML/Data roles requiring modern tooling (LLMs, APIs, cloud infrastructure, production workflows)

Each project is built end-to-end with realistic data and deployment considerations.

## Projects

### 1. Player Churn & Retention System

Predict player churn and analyze retention patterns using simulated mobile game telemetry.

**Skills**: Binary classification, feature engineering, cohort analysis, business metrics  
**Stack**: Python, XGBoost/Random Forest, Pandas, Streamlit  
**Output**: Churn prediction model with interactive retention dashboard

[`01-player-churn-retention/`](01-player-churn-retention/)

### 2. LLM-Powered Support Ticket Intelligence

Retrieval-Augmented Generation system for automated support ticket triage and response.

**Skills**: LLMs, RAG, semantic search, API development  
**Stack**: Python, OpenAI API / Ollama, LangChain, FastAPI, FAISS  
**Output**: REST API for ticket classification and response generation

[`02-support-ticket-rag/`](02-support-ticket-rag/)

### 3. Game Event Analytics Pipeline

ETL pipeline for processing game event streams and generating product metrics.

**Skills**: Data engineering, event processing, aggregation, visualization  
**Stack**: Python, Polars/DuckDB, Streamlit  
**Output**: Event processing pipeline with analytics dashboard

[`03-event-analytics-pipeline/`](03-event-analytics-pipeline/)

### 4. ML Experiment Tracking & Model API

Experiment tracking and model serving infrastructure with containerization.

**Skills**: MLOps, API design, Docker, experiment logging, cloud deployment  
**Stack**: FastAPI, MLflow, Docker, AWS (EC2/ECS)  
**Output**: REST API for model serving with experiment tracking

[`04-ml-experiment-api/`](04-ml-experiment-api/)

## Repository Structure

```
ml-systems-portfolio/
├── 01-player-churn-retention/      # Gaming analytics & churn prediction
├── 02-support-ticket-rag/          # LLM-based RAG system
├── 03-event-analytics-pipeline/    # Event processing & metrics
├── 04-ml-experiment-api/           # MLOps infrastructure
├── shared/                         # Shared utilities and configs
│   ├── data_generators/            # Synthetic data generation
│   └── utils/                      # Common helper functions
├── docs/                           # Technical documentation
├── .gitignore
├── requirements.txt                # Shared Python dependencies
└── README.md
```

---

## Quick Start

**Prerequisites:**
- Python 3.9+
- Docker (for Project 4)
- AWS CLI configured (optional, for cloud deployment)

**Setup:**
```bash
# Clone the repository
git clone https://github.com/ozlem-senel/ml-systems-portfolio.git
cd ml-systems-portfolio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Running Projects:**

Each project has its own README with setup instructions:
- [Player Churn System](01-player-churn-retention/README.md)
- [Support RAG System](02-support-ticket-rag/README.md)
- [Event Pipeline](03-event-analytics-pipeline/README.md)
- [ML API](04-ml-experiment-api/README.md)

## Cloud Integration

Project 4 includes AWS deployment options:
- EC2 for simple model serving
- S3 for model artifacts and datasets
- ECS with ECR for container orchestration

See [`04-ml-experiment-api/docs/aws-deployment.md`](04-ml-experiment-api/docs/aws-deployment.md) for deployment guides.

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.9+ |
| **ML/Data** | Scikit-learn, XGBoost, Pandas, Polars, DuckDB |
| **LLMs** | OpenAI API, LangChain, FAISS, Sentence Transformers |
| **APIs** | FastAPI, Pydantic |
| **Visualization** | Streamlit, Matplotlib, Plotly |
| **MLOps** | MLflow, Docker |
| **Cloud** | AWS (EC2, S3, ECS, ECR) |

---

## 📊 Project Integration
## Project Integration

The projects connect to demonstrate end-to-end system design:
- Project 3 (Event Pipeline) generates data used by Project 1 (Churn Model)
- Projects 1 and 2 models are tracked and served by Project 4 (MLOps API)

## Future Work

- Real-time streaming with Kafka or Redis
- Multi-language support for RAG system
- A/B testing framework
- Kubernetes deployment
- CI/CD pipelines with GitHub Actions

## License

MIT License - See [LICENSE](LICENSE) for details

## Author

Özlem Senel  
Master's student - Data Science & Machine Learning  
[LinkedIn](https://linkedin.com/in/yourprofile) |