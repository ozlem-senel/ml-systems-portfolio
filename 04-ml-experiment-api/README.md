# ML Experiment Tracking & Model API

Experiment tracking and model serving infrastructure with containerization and cloud deployment.

## Objectives

- Build experiment tracking for ML projects
- Serve trained models via REST API
- Containerize with Docker
- Deploy to AWS (EC2 or ECS)

## Business Context

MLOps fundamentals for production systems:
- Experiment tracking prevents unorganized notebook development
- APIs make models accessible to applications
- Docker ensures reproducibility
- Cloud deployment demonstrates production readiness

## Project Structure

```
04-ml-experiment-api/
├── src/
│   ├── api/
│   │   ├── main.py              # FastAPI application
│   │   ├── models/              # Pydantic schemas
│   │   └── routes/              # API endpoints
│   ├── tracking/
│   │   ├── experiment_logger.py # Custom tracking or MLflow
│   │   └── model_registry.py    # Model versioning
│   └── inference/
│       └── predictor.py         # Model loading and inference
├── models/                      # Saved model artifacts
├── experiments/                 # Experiment logs
├── tests/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── api_documentation.md
│   └── aws_deployment.md        # AWS deployment guide
├── requirements.txt
└── README.md
```

## Quick Start

Local development:
```bash
cd 04-ml-experiment-api

# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn src.api.main:app --reload
```

API will be available at `http://localhost:8000`

Docker:
```bash
# Build image
docker build -t ml-api:latest -f docker/Dockerfile .

# Run container
docker run -p 8000:8000 ml-api:latest
```

API documentation:
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

1. Experiment Tracking

Track experiments from Project 1 (Churn Model) and Project 2 (RAG System):
- Model hyperparameters
- Training metrics: accuracy, AUC, loss
- Dataset versions
- Artifact storage: models, plots

Example:
```python
from src.tracking import ExperimentLogger

logger = ExperimentLogger()
logger.log_experiment(
    name="churn_xgboost_v3",
    params={"max_depth": 5, "learning_rate": 0.1},
    metrics={"auc": 0.87, "precision": 0.82},
    artifacts={"model_path": "models/churn_v3.pkl"}
)
```

2. Model Serving API

Endpoints:

POST /predict/churn
```json
{
  "player_id": "user123",
  "sessions_7d": 5,
  "playtime_7d": 120,
  "iap_count": 0
}
```
Response:
```json
{
  "player_id": "user123",
  "churn_probability": 0.73,
  "risk_level": "high",
  "model_version": "v3"
}
```

GET /models - List all available models

GET /experiments - Query experiment history

3. Model Registry
- Version control for models
- Promote models to staging or production
- Rollback capability

4. Health & Monitoring
- /health: API health check
- /metrics: Prometheus-compatible metrics (future)

## Docker & Deployment

Dockerfile features:
- Multi-stage build for smaller image size
- Non-root user for security
- Health check included

AWS deployment options:

Option 1: EC2 (Simple)
1. Launch EC2 instance (t3.small)
2. Install Docker
3. Pull/build image
4. Run container with port forwarding

Cost: approximately $15/month

Option 2: ECS + ECR (Production-like)
1. Push image to ECR (Elastic Container Registry)
2. Create ECS task definition
3. Deploy to Fargate or EC2 cluster
4. Load balancer for high availability

Cost: approximately $30-50/month

See [docs/aws_deployment.md](docs/aws_deployment.md) for deployment guides.

S3 for model storage:
- Store large model files in S3
- API fetches models on startup or on-demand

## Technology Stack

- API Framework: FastAPI (async, fast, auto-docs)
- Tracking: MLflow or custom SQLite-based system
- Containerization: Docker
- Cloud: AWS (EC2, ECS, ECR, S3)
- Model Serialization: Pickle, Joblib, or ONNX

## Integration

Infrastructure for other projects:
- Project 1: Track churn model experiments, serve predictions
- Project 2: Serve RAG endpoints
- Project 3: Could expose analytics as API endpoints

## Skills Demonstrated

- RESTful API design
- MLOps: experiment tracking, model versioning
- Docker containerization
- Cloud deployment with AWS
- Production code: logging, error handling, testing

## Testing

```bash
# Run tests
pytest tests/

# API endpoint tests
pytest tests/test_api.py

# Load testing (optional)
locust -f tests/load_test.py
```

## Monitoring & Logging

- Structured logging in JSON format
- Request and response logging
- Error tracking
- Future: Prometheus and Grafana dashboards

## Future Work

- CI/CD pipeline with GitHub Actions
- Kubernetes deployment
- Model A/B testing framework
- Real-time monitoring dashboard
- Authentication and API keys
