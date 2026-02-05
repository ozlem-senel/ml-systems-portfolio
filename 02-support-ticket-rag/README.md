# LLM-Powered Support Ticket Intelligence

Retrieval-Augmented Generation system for automated support ticket classification and response generation.

## Objectives

- Build a RAG pipeline for customer support automation
- Classify incoming tickets by category and urgency
- Generate relevant response suggestions using LLMs
- Provide a REST API for integration

## Business Context

Support teams handle thousands of tickets daily across categories like payment issues, bug reports, account help, and feature requests. Manual triage is slow and inconsistent. This system automates initial response and routing to reduce resolution time.

## Project Structure

```
02-support-ticket-rag/
├── data/
│   ├── tickets/              # Synthetic support tickets
│   └── knowledge_base/       # FAQ and help documents
├── notebooks/
│   ├── 01_data_creation.ipynb
│   ├── 02_rag_prototype.ipynb
│   └── 03_evaluation.ipynb
├── src/
│   ├── data_generator.py     # Generate synthetic tickets
│   ├── embeddings.py         # Create vector embeddings
│   ├── rag_pipeline.py       # RAG implementation
│   ├── api.py                # FastAPI endpoint
│   └── evaluation.py         # Quality metrics
├── models/                   # Embedding models
├── vector_store/             # FAISS index
├── tests/
├── requirements.txt
└── README.md
```

## Quick Start

**Setup:**
```bash
cd 02-support-ticket-rag

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key or use Ollama locally
export OPENAI_API_KEY="your-key-here"

# Generate data
python src/data_generator.py

# Build vector store
python src/embeddings.py

# Start API
uvicorn src.api:app --reload
```

**API Usage:**
```bash
# Classify and respond to a ticket
curl -X POST "http://localhost:8000/ticket/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "I cant log in to my account", "ticket_id": "12345"}'
```

**Response**:
```json
{
  "ticket_id": "12345",
  "category": "account_access",
  "urgency": "high",
  "suggested_response": "I understand you're having trouble logging in...",
  "relevant_docs": ["FAQ: Password Reset", "Guide: Account Recovery"]
}
```

## Features

**RAG Pipeline:**
1. Embedding: Convert tickets and knowledge base to vectors using Sentence Transformers
2. Retrieval: Semantic search with FAISS to find relevant documents
3. Generation: Use retrieved context with LLM to generate responses

**Categories:**
- payment_issue: IAP problems, refunds
- bug_report: Technical issues
- account_access: Login, password reset
- feature_request: New features or improvements
- general_inquiry: Other questions

**LLM Options:**
- OpenAI GPT-4: High quality, requires API key
- Ollama with Llama 3: Local, free

## Methodology

1. Data Generation: Create 1,000+ realistic support tickets
2. Knowledge Base: Build FAQ with common solutions
3. Embedding Model: Use all-MiniLM-L6-v2 for semantic similarity
4. Prompt Engineering: Optimize LLM prompts for clarity and helpfulness
5. Evaluation: Measure classification accuracy, response quality, latency

## Evaluation Metrics

- Classification Accuracy: 90%+ on test set
- Retrieval Relevance: Top-3 documents contain answer 85% of time
- Response Quality: Evaluated for clarity and helpfulness
- Latency: Under 2 seconds per ticket

## Integration

- API served via Project 4 (ML Experiment API infrastructure)
- Could analyze ticket trends using Project 3 (Event Pipeline)

## Skills Demonstrated

- RAG system design and implementation
- LLM prompt engineering
- Vector embeddings and semantic search
- FastAPI development
- Evaluation of generative AI systems

## Future Work

- Multi-turn conversation support
- Fine-tuned classification model
- Feedback loop for continuous improvement
- Multi-language support

---

Status: In Progress | Last Updated: Feb 2026
