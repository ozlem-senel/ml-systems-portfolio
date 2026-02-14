# Support Ticket RAG System

AI-powered support ticket processing using Retrieval-Augmented Generation (RAG) with LLMs.

## Overview

This system automatically processes customer support tickets by:
1. Retrieving relevant knowledge base articles using semantic search
2. Classifying ticket category and urgency level
3. Generating context-aware responses using AI

## Features

- Semantic search: Uses sentence-transformers for vector embeddings
- Multiple LLM support: Mock (templates), OpenAI GPT, or Google Gemini
- RESTful API: FastAPI endpoint for easy integration
- High performance: Processes tickets in <1 second
- Free tier option: Works with free Gemini API (1500 requests/day)

## Architecture

```
Support Ticket → Embeddings → Vector Search → Top-K Docs → LLM → Response
                    ↓                           ↓
              Knowledge Base              Classification
```

## Dataset

Support tickets: 500 synthetic tickets across 4 categories
  - Payment issues (26%)
  - Bug reports (25.8%)
  - Feature requests (26.4%)
  - Account management (21.8%)

Knowledge base: 15 curated documents with solutions

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```bash
# Choose LLM provider: mock, openai, or gemini
LLM_PROVIDER=gemini

# For Gemini (free tier - 1500 requests/day)
GOOGLE_API_KEY=your-api-key-here

# For OpenAI (paid)
OPENAI_API_KEY=your-api-key-here
```

## Usage

### 1. Generate Data (Already Done)

```bash
python src/data_generator.py
python src/knowledge_base.py
```

### 2. Build Vector Store (Already Done)

```bash
python src/embeddings.py
```

### 3. Test RAG Pipeline

```bash
python src/rag_pipeline.py
```

### 4. Start API Server

```bash
python src/api.py
```

Or with uvicorn:
```bash
uvicorn src.api:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- API info: http://localhost:8000/

### Endpoints

POST /process - Process a support ticket and get AI-generated response.

Request:
```json
{
  "ticket_id": "TICKET-001",
  "subject": "Payment failed",
  "description": "My credit card was declined but I have funds",
  "category": "payment"
}
```

Response:
```json
{
  "ticket_id": "TICKET-001",
  "predicted_category": "payment",
  "urgency": "high",
  "confidence": 0.85,
  "response": "Thank you for contacting us about your payment issue...",
  "retrieved_documents": [
    {"title": "Payment Failed - Insufficient Funds", "score": 0.89}
  ]
}
```

GET /health - Check API health status.

### Example Usage

cURL:
```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TEST-001",
    "subject": "App crashes on startup",
    "description": "The mobile app crashes immediately after opening"
  }'
```

Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/process",
    json={
        "ticket_id": "TEST-001",
        "subject": "App crashes on startup",
        "description": "The mobile app crashes immediately after opening"
    }
)
print(response.json())
```

## Performance

- Retrieval accuracy: 0.619-0.785 similarity scores for top documents
- Classification: 100% accuracy on test cases
- Response time: <1 second per ticket
- Vector store size: 15 documents, 384 dimensions

## Tech Stack

- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector store: scikit-learn NearestNeighbors
- LLM: Google Gemini 2.5 Flash (free tier)
- API: FastAPI + uvicorn
- Data: Python, pandas, JSON

## Results

Successfully processes support tickets with:
- Correct category classification (payment, bug, account, feature)
- Appropriate urgency levels (low, medium, high, critical)
- Context-aware responses based on knowledge base
- Real-time AI generation with Gemini API

## Project Structure

```
02-support-ticket-rag/
├── src/
│   ├── data_generator.py      # Generate synthetic tickets
│   ├── knowledge_base.py      # Create KB documents
│   ├── embeddings.py          # Build vector store
│   ├── rag_pipeline.py        # Core RAG logic
│   └── api.py                 # FastAPI endpoint
├── data/
│   ├── tickets/               # Support tickets (500)
│   └── knowledge_base/        # KB documents (15)
├── vector_store/
│   └── vector_store.pkl       # Embeddings + sklearn model
├── test_api.py                # API test script
├── requirements.txt
├── .env.example
└── README.md
```

## Future Improvements

- Add evaluation metrics (BLEU, ROUGE scores)
- Implement caching for faster responses
- Add user feedback loop for response quality
- Expand knowledge base to 100+ documents
- Support multi-language tickets
- Add ticket routing to human agents

## License

MIT
