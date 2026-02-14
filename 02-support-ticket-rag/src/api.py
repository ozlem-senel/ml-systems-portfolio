"""FastAPI endpoint for Support Ticket RAG system."""
import os
import sys
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rag_pipeline import RAGPipeline

load_dotenv()

app = FastAPI(
    title="Support Ticket RAG API",
    description="AI-powered support ticket processing using RAG and LLMs",
    version="1.0.0"
)

pipeline = None


class TicketRequest(BaseModel):
    """Request model for ticket processing."""
    ticket_id: str
    subject: str
    description: str
    category: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": "TICKET-001",
                "subject": "Payment failed",
                "description": "My credit card payment was declined but I have sufficient funds",
                "category": "payment"
            }
        }


class TicketResponse(BaseModel):
    """Response model for processed ticket."""
    ticket_id: str
    predicted_category: str
    urgency: str
    confidence: float
    response: str
    retrieved_documents: List[Dict]
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": "TICKET-001",
                "predicted_category": "payment",
                "urgency": "high",
                "confidence": 0.85,
                "response": "Thank you for contacting us about your payment issue...",
                "retrieved_documents": [
                    {"title": "Payment Failed - Insufficient Funds", "score": 0.89}
                ]
            }
        }


@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup."""
    global pipeline
    llm_provider = os.getenv('LLM_PROVIDER', 'mock').lower()
    vector_store_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'vector_store'
    )
    
    # Get API key if needed
    api_key = None
    if llm_provider == 'gemini':
        api_key = os.getenv('GOOGLE_API_KEY')
    elif llm_provider == 'openai':
        api_key = os.getenv('OPENAI_API_KEY')
    
    pipeline = RAGPipeline(
        llm_provider=llm_provider, 
        vector_store_path=vector_store_dir,
        api_key=api_key
    )
    print(f"RAG pipeline initialized with {llm_provider} LLM")


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Support Ticket RAG API",
        "version": "1.0.0",
        "status": "running",
        "llm_provider": os.getenv('LLM_PROVIDER', 'mock'),
        "endpoints": {
            "process_ticket": "/process",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "pipeline_ready": pipeline is not None,
        "llm_provider": os.getenv('LLM_PROVIDER', 'mock')
    }


@app.post("/process", response_model=TicketResponse)
async def process_ticket(ticket: TicketRequest):
    """
    Process a support ticket using RAG pipeline.
    
    This endpoint:
    1. Retrieves relevant knowledge base documents
    2. Classifies the ticket category and urgency
    3. Generates an AI-powered response
    
    Args:
        ticket: Support ticket details
        
    Returns:
        Processed ticket with classification and AI-generated response
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    try:
        ticket_dict = {
            'ticket_id': ticket.ticket_id,
            'subject': ticket.subject,
            'description': ticket.description,
            'category': ticket.category
        }
        
        result = pipeline.process_ticket(ticket_dict)
        
        return TicketResponse(
            ticket_id=ticket.ticket_id,
            predicted_category=result['classification']['predicted_category'],
            urgency=result['classification']['urgency'],
            confidence=result['classification']['confidence'],
            response=result['response'],
            retrieved_documents=[
                {"title": doc['title'], "score": doc['relevance_score']}
                for doc in result['context_documents']
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing ticket: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
