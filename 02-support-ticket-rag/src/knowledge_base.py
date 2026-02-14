"""
Knowledge base documents for RAG retrieval.
These serve as the source of information for generating responses.
"""

KNOWLEDGE_BASE = [
    {
        "doc_id": "KB001",
        "category": "payment",
        "title": "Payment Failed - Insufficient Funds",
        "content": """
If your payment failed due to insufficient funds, please check your account balance 
and ensure you have enough funds available. You can retry the payment once you've 
added funds to your account. If the issue persists, try using a different payment method.
"""
    },
    {
        "doc_id": "KB002",
        "category": "payment",
        "title": "Refund Process",
        "content": """
To request a refund, please provide your transaction ID and reason for the refund. 
Refunds are typically processed within 5-7 business days. You will receive an email 
confirmation once the refund has been initiated. Please note that it may take an 
additional 3-5 days for the funds to appear in your account depending on your bank.
"""
    },
    {
        "doc_id": "KB003",
        "category": "payment",
        "title": "Credit Card Declined",
        "content": """
If your credit card is declined, this could be due to several reasons:
1. Insufficient funds
2. Card expired
3. Incorrect card details entered
4. Bank fraud prevention
Please verify your card details and contact your bank if the issue persists.
"""
    },
    {
        "doc_id": "KB004",
        "category": "payment",
        "title": "Double Charge Resolution",
        "content": """
If you were charged twice for the same transaction, we apologize for the inconvenience. 
Please provide your transaction IDs for both charges. One charge may be a pending 
authorization that will drop off within 3-5 business days. If both charges posted, 
we will immediately refund the duplicate charge.
"""
    },
    {
        "doc_id": "KB005",
        "category": "bug",
        "title": "App Crashes on Startup",
        "content": """
If the app crashes immediately after opening, try these troubleshooting steps:
1. Force close the app and restart
2. Clear app cache (Settings > Apps > [App Name] > Clear Cache)
3. Update to the latest version
4. Uninstall and reinstall the app
5. Restart your device
If the problem persists, please provide your device model and OS version.
"""
    },
    {
        "doc_id": "KB006",
        "category": "bug",
        "title": "Login Issues Resolution",
        "content": """
If you're experiencing login issues:
1. Verify your username and password are correct
2. Check if Caps Lock is on
3. Clear browser cache and cookies
4. Try a different browser or device
5. Use the 'Forgot Password' feature to reset your password
If none of these work, your account may be temporarily locked for security reasons.
"""
    },
    {
        "doc_id": "KB007",
        "category": "bug",
        "title": "Data Sync Problems",
        "content": """
If your data is not syncing across devices:
1. Ensure you're logged into the same account on all devices
2. Check your internet connection
3. Enable sync in Settings > Sync & Backup
4. Force a manual sync by pulling down on the main screen
5. Sign out and sign back in on the affected device
Data typically syncs within 1-2 minutes when connected to the internet.
"""
    },
    {
        "doc_id": "KB008",
        "category": "bug",
        "title": "Performance and Speed Issues",
        "content": """
If the app is running slowly:
1. Close other apps running in the background
2. Clear app cache
3. Check available storage space (need at least 500MB free)
4. Update to the latest app version
5. Restart your device
Performance issues often occur when device storage is low or too many apps are running.
"""
    },
    {
        "doc_id": "KB009",
        "category": "account",
        "title": "Account Locked - Security",
        "content": """
Your account may be locked due to:
1. Multiple failed login attempts
2. Suspicious activity detected
3. Terms of service violation
For security reasons, accounts are automatically unlocked after 24 hours. 
If you need immediate access, please verify your identity by responding with:
- Email address on file
- Last 4 digits of payment method
- Date of last successful login
"""
    },
    {
        "doc_id": "KB010",
        "category": "account",
        "title": "Password Reset Process",
        "content": """
To reset your password:
1. Click 'Forgot Password' on the login page
2. Enter your email address
3. Check your email for reset link (check spam folder)
4. Click the link and create a new password
5. Password must be at least 8 characters with one uppercase, one number
If you don't receive the email within 10 minutes, check your spam folder or try again.
"""
    },
    {
        "doc_id": "KB011",
        "category": "account",
        "title": "Email Address Change",
        "content": """
To change your email address:
1. Log in to your account
2. Go to Settings > Account > Email
3. Enter your new email address
4. Verify the change via email sent to both old and new addresses
For security, you'll need to verify your identity by entering your current password.
"""
    },
    {
        "doc_id": "KB012",
        "category": "account",
        "title": "Account Deletion Process",
        "content": """
To delete your account:
1. Go to Settings > Account > Delete Account
2. Review what will be deleted (this is permanent)
3. Enter your password to confirm
4. Click 'Delete Account'
Please note: Account deletion is permanent and cannot be undone. All your data, 
purchases, and settings will be permanently deleted within 30 days.
"""
    },
    {
        "doc_id": "KB013",
        "category": "account",
        "title": "Subscription Management",
        "content": """
To manage your subscription:
1. Go to Settings > Subscription
2. View current plan and billing date
3. Options available:
   - Upgrade/Downgrade plan
   - Cancel subscription
   - Update payment method
   - View billing history
Cancellations take effect at the end of the current billing period.
"""
    },
    {
        "doc_id": "KB014",
        "category": "feature",
        "title": "Feature Availability by Region",
        "content": """
Some features may not be available in all regions due to:
1. Local regulations and compliance requirements
2. Licensing restrictions
3. Infrastructure limitations
4. Gradual rollout process
Check Settings > About > Available Features to see what's enabled in your region.
We're constantly working to expand feature availability globally.
"""
    },
    {
        "doc_id": "KB015",
        "category": "feature",
        "title": "Feature Request Process",
        "content": """
We welcome feature requests! To submit a request:
1. Go to Settings > Feedback > Feature Request
2. Describe the feature and how it would help you
3. Our product team reviews all requests monthly
4. Popular requests are added to our roadmap
You can also vote on existing feature requests in our community forum.
"""
    },
]


def save_knowledge_base():
    """Save knowledge base to JSON file."""
    import json
    from pathlib import Path
    
    output_path = Path('data/knowledge_base/kb_documents.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(KNOWLEDGE_BASE, f, indent=2)
    
    print(f"Saved {len(KNOWLEDGE_BASE)} knowledge base documents to {output_path}")


if __name__ == '__main__':
    save_knowledge_base()
