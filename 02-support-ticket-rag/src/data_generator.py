"""
Generate synthetic support tickets for RAG system training and evaluation.
Creates realistic tickets across multiple categories with varying urgency levels.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


class TicketGenerator:
    """Generate synthetic customer support tickets."""
    
    CATEGORIES = {
        'payment': {
            'subjects': [
                'Payment failed',
                'Refund request',
                'Credit card declined',
                'Billing error',
                'Double charge issue',
                'Payment method not working',
            ],
            'issues': [
                'My payment was declined but I have sufficient funds.',
                'I was charged twice for the same purchase.',
                'I need a refund for my last transaction.',
                'My credit card is not being accepted.',
                'The billing amount is incorrect.',
                'Payment processing is taking too long.',
            ]
        },
        'bug': {
            'subjects': [
                'App crashes on startup',
                'Features not working',
                'Login issues',
                'Data sync problems',
                'Performance issues',
                'UI glitches',
            ],
            'issues': [
                'The app crashes immediately after opening.',
                'Cannot login with my credentials.',
                'My data is not syncing across devices.',
                'The app is extremely slow and laggy.',
                'Some features are completely broken.',
                'UI elements are overlapping and unreadable.',
            ]
        },
        'account': {
            'subjects': [
                'Account locked',
                'Password reset help',
                'Email change request',
                'Delete account',
                'Account recovery',
                'Subscription management',
            ],
            'issues': [
                'My account has been locked and I cannot access it.',
                'I forgot my password and the reset email is not arriving.',
                'I need to change my email address.',
                'I want to delete my account permanently.',
                'I cannot recover my account after losing access.',
                'I need help managing my subscription.',
            ]
        },
        'feature': {
            'subjects': [
                'Feature request',
                'How to use feature',
                'Feature not available',
                'Missing functionality',
                'Feature improvement suggestion',
            ],
            'issues': [
                'Can you add dark mode to the app?',
                'How do I use the export feature?',
                'This feature is not available in my region.',
                'The app is missing basic functionality.',
                'I have suggestions to improve this feature.',
            ]
        }
    }
    
    URGENCY_LEVELS = ['low', 'medium', 'high', 'critical']
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        
    def generate_ticket(self, ticket_id: int) -> Dict:
        """Generate a single support ticket."""
        category = random.choice(list(self.CATEGORIES.keys()))
        category_data = self.CATEGORIES[category]
        
        # Determine urgency based on category
        if category == 'payment':
            urgency_weights = [0.1, 0.3, 0.4, 0.2]  # More likely high/critical
        elif category == 'bug':
            urgency_weights = [0.2, 0.4, 0.3, 0.1]  # Balanced
        elif category == 'account':
            urgency_weights = [0.15, 0.35, 0.4, 0.1]  # Slightly higher
        else:  # feature
            urgency_weights = [0.5, 0.35, 0.15, 0.0]  # Mostly low/medium
            
        urgency = random.choices(self.URGENCY_LEVELS, weights=urgency_weights)[0]
        
        # Generate timestamp (last 30 days)
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago)
        
        ticket = {
            'ticket_id': f'TKT-{ticket_id:06d}',
            'timestamp': timestamp.isoformat(),
            'category': category,
            'urgency': urgency,
            'subject': random.choice(category_data['subjects']),
            'description': random.choice(category_data['issues']),
            'customer_id': f'CUST-{random.randint(1000, 9999)}',
            'status': random.choice(['open', 'in_progress', 'resolved', 'closed']),
        }
        
        return ticket
    
    def generate_dataset(self, num_tickets: int = 500) -> List[Dict]:
        """Generate a dataset of support tickets."""
        tickets = [self.generate_ticket(i) for i in range(1, num_tickets + 1)]
        return tickets
    
    def save_tickets(self, tickets: List[Dict], output_path: str):
        """Save tickets to JSONL file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            for ticket in tickets:
                f.write(json.dumps(ticket) + '\n')
        
        print(f"Generated {len(tickets)} tickets")
        print(f"Saved to: {output_file}")
        
        # Print statistics
        categories = {}
        urgencies = {}
        for ticket in tickets:
            categories[ticket['category']] = categories.get(ticket['category'], 0) + 1
            urgencies[ticket['urgency']] = urgencies.get(ticket['urgency'], 0) + 1
        
        print("\nCategory Distribution:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count} ({count/len(tickets)*100:.1f}%)")
        
        print("\nUrgency Distribution:")
        for urg, count in sorted(urgencies.items()):
            print(f"  {urg}: {count} ({count/len(tickets)*100:.1f}%)")


def main():
    """Generate synthetic support tickets."""
    generator = TicketGenerator(seed=42)
    tickets = generator.generate_dataset(num_tickets=500)
    generator.save_tickets(tickets, 'data/tickets/support_tickets.jsonl')


if __name__ == '__main__':
    main()
