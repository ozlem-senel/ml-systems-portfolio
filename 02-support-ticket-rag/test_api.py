"""Test script for Support Ticket RAG API."""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """Test all API endpoints."""
    
    print("=" * 70)
    print("TESTING SUPPORT TICKET RAG API")
    print("=" * 70)
    
    # Test root endpoint
    print("\n1. Testing root endpoint (GET /)...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test health check
    print("\n2. Testing health check (GET /health)...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test ticket processing
    print("\n3. Testing ticket processing (POST /process)...")
    
    test_tickets = [
        {
            "ticket_id": "TEST-001",
            "subject": "Payment failed",
            "description": "My credit card payment was declined but I have sufficient funds in my account"
        },
        {
            "ticket_id": "TEST-002",
            "subject": "App crashes on startup",
            "description": "The mobile app crashes immediately after I open it"
        },
        {
            "ticket_id": "TEST-003",
            "subject": "Cannot login to my account",
            "description": "I forgot my password and need to reset it"
        }
    ]
    
    for ticket in test_tickets:
        print(f"\n{'=' * 70}")
        print(f"Processing: {ticket['subject']}")
        print("=" * 70)
        
        response = requests.post(
            f"{BASE_URL}/process",
            json=ticket
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nTicket ID: {result['ticket_id']}")
            print(f"Category: {result['predicted_category']}")
            print(f"Urgency: {result['urgency']}")
            print(f"Confidence: {result['confidence']:.3f}")
            print(f"\nRetrieved Documents:")
            for doc in result['retrieved_documents']:
                print(f"  - {doc['title']} (score: {doc['score']:.3f})")
            print(f"\nGenerated Response:")
            print(result['response'][:200] + "..." if len(result['response']) > 200 else result['response'])
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running: python src/api.py")
