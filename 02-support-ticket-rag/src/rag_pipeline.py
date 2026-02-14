"""
RAG pipeline for support ticket classification and response generation.
Supports both OpenAI API and mock mode for portfolio demonstration.
"""

import os
from typing import List, Dict, Optional
from pathlib import Path

from embeddings import EmbeddingManager


class MockLLM:
    """Mock LLM for demonstration without API costs."""
    
    def generate_response(self, ticket: Dict, context_docs: List[Dict]) -> str:
        """Generate template-based response."""
        category = ticket.get('category', 'general')
        
        # Use the most relevant document
        if context_docs:
            top_doc = context_docs[0]
            # Extract key information from the document
            content = top_doc['content'].strip()
            
            response = f"""Based on your {category} inquiry, here's what you need to know:

{content}

If you need further assistance, please provide additional details about your specific situation.

Reference: {top_doc['doc_id']} - {top_doc['title']}"""
        else:
            response = f"""Thank you for contacting support regarding your {category} issue.

I understand you're experiencing difficulties. To help you better, could you please provide:
1. More details about the issue
2. Any error messages you're seeing
3. Steps you've already tried

Our team will review your ticket and respond within 24 hours."""
        
        return response
    
    def classify_ticket(self, ticket: Dict, context_docs: List[Dict]) -> Dict:
        """Classify ticket using document matches."""
        if context_docs:
            category = context_docs[0]['category']
            confidence = context_docs[0]['score']
        else:
            category = ticket.get('category', 'general')
            confidence = 0.5
        
        # Determine urgency based on keywords
        description = ticket.get('description', '').lower()
        urgency_keywords = {
            'critical': ['cannot login', 'account locked', 'double charge', 'charged twice'],
            'high': ['payment failed', 'app crashes', 'not working'],
            'medium': ['slow', 'issue', 'problem'],
            'low': ['request', 'how to', 'feature']
        }
        
        urgency = 'low'
        for level, keywords in urgency_keywords.items():
            if any(kw in description for kw in keywords):
                urgency = level
                break
        
        return {
            'predicted_category': category,
            'confidence': confidence,
            'urgency': urgency,
            'reasoning': f"Matched with {context_docs[0]['title']}" if context_docs else "No strong match"
        }


class GeminiLLM:
    """Google Gemini integration"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """Initialize Gemini client with new google.genai package."""
        try:
            from google import genai
            from google.genai import types
            self.client = genai.Client(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("Google GenAI package not installed. Run: pip install google-genai")
    
    def generate_response(self, ticket: Dict, context_docs: List[Dict]) -> str:
        """Generate response using Gemini API."""
        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1} ({doc['title']}):\n{doc['content']}"
            for i, doc in enumerate(context_docs[:3])
        ])
        
        prompt = f"""You are a customer support assistant. Based on the following support ticket and knowledge base documents, generate a helpful response.

Support Ticket:
Subject: {ticket.get('subject', 'No subject')}
Description: {ticket.get('description', 'No description')}
Category: {ticket.get('category', 'Unknown')}

Relevant Knowledge Base:
{context}

Generate a professional, helpful response that addresses the customer's issue. Include specific steps or information from the knowledge base. Keep the response concise (under 200 words)."""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
    
    def classify_ticket(self, ticket: Dict, context_docs: List[Dict]) -> Dict:
        """Classify ticket using Gemini."""
        context = "\n".join([f"- {doc['category']}: {doc['title']}" for doc in context_docs[:3]])
        
        prompt = f"""Classify this support ticket into one of these categories: payment, bug, account, feature.
Also determine urgency level: low, medium, high, critical.

Ticket:
Subject: {ticket.get('subject', 'No subject')}
Description: {ticket.get('description', 'No description')}

Similar tickets were categorized as:
{context}

Respond in this exact format:
Category: [category]
Urgency: [urgency]
Reasoning: [brief explanation]"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        text = response.text.strip()
        lines = text.split('\n')
        
        result = {
            'predicted_category': 'general',
            'urgency': 'medium',
            'reasoning': text,
            'confidence': context_docs[0]['score'] if context_docs else 0.5
        }
        
        for line in lines:
            if 'Category:' in line:
                result['predicted_category'] = line.split(':')[1].strip().lower()
            elif 'Urgency:' in line:
                result['urgency'] = line.split(':')[1].strip().lower()
        
        return result


class OpenAILLM:
    """OpenAI GPT integration for real LLM responses."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """Initialize OpenAI client."""
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate_response(self, ticket: Dict, context_docs: List[Dict]) -> str:
        """Generate response using OpenAI API."""
        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document {i+1} ({doc['title']}):\n{doc['content']}"
            for i, doc in enumerate(context_docs[:3])
        ])
        
        prompt = f"""You are a customer support assistant. Based on the following support ticket and knowledge base documents, generate a helpful response.

Support Ticket:
Subject: {ticket.get('subject', 'No subject')}
Description: {ticket.get('description', 'No description')}
Category: {ticket.get('category', 'Unknown')}

Relevant Knowledge Base:
{context}

Generate a professional, helpful response that addresses the customer's issue. Include specific steps or information from the knowledge base."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
    
    def classify_ticket(self, ticket: Dict, context_docs: List[Dict]) -> Dict:
        """Classify ticket using OpenAI."""
        context = "\n".join([f"- {doc['category']}: {doc['title']}" for doc in context_docs[:3]])
        
        prompt = f"""Classify this support ticket into one of these categories: payment, bug, account, feature.
Also determine urgency level: low, medium, high, critical.

Ticket:
Subject: {ticket.get('subject', 'No subject')}
Description: {ticket.get('description', 'No description')}

Similar tickets were categorized as:
{context}

Respond in this format:
Category: [category]
Urgency: [urgency]
Reasoning: [brief explanation]"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100
        )
        
        text = response.choices[0].message.content
        lines = text.strip().split('\n')
        
        result = {
            'predicted_category': 'general',
            'urgency': 'medium',
            'reasoning': text
        }
        
        for line in lines:
            if 'Category:' in line:
                result['predicted_category'] = line.split(':')[1].strip().lower()
            elif 'Urgency:' in line:
                result['urgency'] = line.split(':')[1].strip().lower()
        
        return result


class RAGPipeline:
    """Main RAG pipeline for ticket processing."""
    
    def __init__(self, vector_store_path: str, llm_provider: str = 'mock', api_key: Optional[str] = None):
        """
        Initialize RAG pipeline.
        
        Args:
            vector_store_path: Path to saved vector store
            llm_provider: 'openai', 'gemini', or 'mock'
            api_key: API key for OpenAI or Gemini (required if not using mock)
        """
        print(f"Initializing RAG pipeline with {llm_provider} LLM...")
        
        # Load vector store
        self.embedding_manager = EmbeddingManager.load(
            model_name='all-MiniLM-L6-v2',
            index_dir=vector_store_path
        )
        
        # Initialize LLM
        if llm_provider == 'openai':
            if not api_key:
                raise ValueError("OpenAI API key required when llm_provider='openai'")
            self.llm = OpenAILLM(api_key=api_key)
        elif llm_provider == 'gemini':
            if not api_key:
                raise ValueError("Google API key required when llm_provider='gemini'")
            self.llm = GeminiLLM(api_key=api_key)
        else:
            self.llm = MockLLM()
        
        print("Pipeline ready!")
    
    def process_ticket(self, ticket: Dict, k: int = 3) -> Dict:
        """
        Process a support ticket through the RAG pipeline.
        
        Args:
            ticket: Ticket dictionary with subject, description, etc.
            k: Number of relevant documents to retrieve
            
        Returns:
            Dictionary with classification, response, and context docs
        """
        # Create search query from ticket
        query = f"{ticket.get('subject', '')} {ticket.get('description', '')}"
        
        # Retrieve relevant documents
        context_docs = self.embedding_manager.search(query, k=k)
        
        # Classify ticket
        classification = self.llm.classify_ticket(ticket, context_docs)
        
        # Generate response
        response = self.llm.generate_response(ticket, context_docs)
        
        return {
            'ticket_id': ticket.get('ticket_id', 'UNKNOWN'),
            'classification': classification,
            'response': response,
            'context_documents': [
                {
                    'doc_id': doc['doc_id'],
                    'title': doc['title'],
                    'category': doc['category'],
                    'relevance_score': doc['score']
                }
                for doc in context_docs
            ]
        }


def main():
    """Demo the RAG pipeline."""
    import json
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    llm_provider = os.getenv('LLM_PROVIDER', 'mock')
    api_key = os.getenv('OPENAI_API_KEY') if llm_provider == 'openai' else os.getenv('GOOGLE_API_KEY')
    
    # Initialize pipeline
    pipeline = RAGPipeline(
        vector_store_path='vector_store',
        llm_provider=llm_provider,
        api_key=api_key
    )
    
    # Test with sample tickets
    test_tickets = [
        {
            'ticket_id': 'TEST-001',
            'subject': 'Payment failed',
            'description': 'My payment was declined but I have sufficient funds.',
            'category': 'payment'
        },
        {
            'ticket_id': 'TEST-002',
            'subject': 'App crashes',
            'description': 'The app crashes immediately after opening.',
            'category': 'bug'
        },
        {
            'ticket_id': 'TEST-003',
            'subject': 'Password reset',
            'description': 'I forgot my password and need to reset it.',
            'category': 'account'
        }
    ]
    
    print("\n" + "="*70)
    print("TESTING RAG PIPELINE")
    print("="*70)
    
    for ticket in test_tickets:
        print(f"\n{'='*70}")
        print(f"TICKET: {ticket['ticket_id']} - {ticket['subject']}")
        print(f"{'='*70}")
        
        result = pipeline.process_ticket(ticket)
        
        print(f"\nCLASSIFICATION:")
        print(f"  Category: {result['classification']['predicted_category']}")
        print(f"  Urgency: {result['classification']['urgency']}")
        
        print(f"\nRETRIEVED DOCUMENTS:")
        for doc in result['context_documents']:
            print(f"  - {doc['title']} (score: {doc['relevance_score']:.3f})")
        
        print(f"\nGENERATED RESPONSE:")
        print(result['response'])
        
        # Save result
        output_dir = Path('data/results')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / f"{ticket['ticket_id']}_result.json", 'w') as f:
            json.dump(result, f, indent=2)


if __name__ == '__main__':
    main()
