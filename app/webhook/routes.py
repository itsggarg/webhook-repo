"""
GitHub Webhook Routes Module
===========================
This module handles incoming webhooks from GitHub for repository events.
It processes push, pull request, and merge events, verifies their authenticity,
and stores them in MongoDB for display in the UI.

Security:
    - Implements HMAC signature verification to ensure webhooks are from GitHub
    - Validates payload structure before processing

Supported Events:
    - push: When commits are pushed to a repository
    - pull_request: When PRs are opened, reopened, or closed
    - merge: When a PR is merged (special case of pull_request closed)
"""

from flask import Blueprint, json, request, jsonify
from datetime import datetime
import hmac
import hashlib
from app.extensions import mongo

# Create a Blueprint for webhook routes
# This groups all webhook-related routes under the /webhook prefix
# Blueprint allows modular organization of routes
webhook = Blueprint(
    'Webhook',           # Blueprint name (used for url_for)
    __name__,           # Import name
    url_prefix='/webhook'  # All routes in this blueprint will be prefixed with /webhook
)


def verify_webhook_signature(payload_body, signature_header, secret):
    """
    Verify that the webhook payload was sent from GitHub.
    
    GitHub signs webhook payloads using HMAC-SHA256 with a shared secret.
    This function verifies that signature to ensure the webhook is authentic
    and hasn't been tampered with.
    
    Args:
        payload_body (bytes): The raw request body
        signature_header (str): The X-Hub-Signature-256 header value
        secret (str): The webhook secret configured in GitHub and our app
    
    Returns:
        bool: True if signature is valid, False otherwise
    
    Security Note:
        This is critical for webhook security. Without verification, anyone
        could send fake webhook events to your endpoint.
    
    GitHub's Process:
        1. GitHub creates HMAC-SHA256 hash of payload using the secret
        2. Sends hash in X-Hub-Signature-256 header as "sha256=<hash>"
        3. We recreate the hash and compare
    """
    
    # Skip verification if no secret is configured (development only!)
    # This is a security risk and should only be used for testing
    if not secret or secret == 'your-webhook-secret-here':
        return True
    
    # If secret is configured but no signature provided, reject
    if not signature_header:
        return False
    
    # Create HMAC-SHA256 hash of the payload using our secret
    # This recreates what GitHub should have sent
    hash_object = hmac.new(
        secret.encode('utf-8'),      # Secret must be bytes
        msg=payload_body,            # Original payload bytes
        digestmod=hashlib.sha256     # Use SHA256 algorithm
    )
    
    # Format the hash as GitHub does: "sha256=<hex_digest>"
    expected_signature = "sha256=" + hash_object.hexdigest()
    
    # Use compare_digest for timing-attack-safe comparison
    # Regular == comparison can leak information through timing
    return hmac.compare_digest(expected_signature, signature_header)


@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    Main webhook endpoint that receives and processes GitHub events.
    
    This endpoint:
    1. Receives POST requests from GitHub webhooks
    2. Verifies the signature for security
    3. Parses the event type and payload
    4. Extracts relevant information based on event type
    5. Stores the event in MongoDB
    6. Returns appropriate HTTP response
    
    Expected Headers:
        X-GitHub-Event: The type of event (push, pull_request, etc.)
        X-Hub-Signature-256: HMAC signature for verification
        Content-Type: Should be application/json
    
    Returns:
        tuple: (response_json, status_code)
        - 200: Event processed successfully
        - 400: Bad request (invalid JSON, missing payload)
        - 401: Unauthorized (invalid signature)
        - 500: Server error (database issues)
    """
    
    # Log webhook receipt for debugging
    print("\n=== WEBHOOK RECEIVED ===")
    
    # Extract important headers
    # X-GitHub-Event tells us what type of event this is
    event_type = request.headers.get('X-GitHub-Event')
    # X-Hub-Signature-256 contains the HMAC signature for verification
    signature = request.headers.get('X-Hub-Signature-256')
    
    # Log event details for debugging
    print(f"Event Type: {event_type}")
    print(f"Content-Type: {request.headers.get('Content-Type')}")
    
    # Get webhook secret from app configuration
    # current_app is a proxy to the active Flask application
    from flask import current_app
    webhook_secret = current_app.config.get('WEBHOOK_SECRET')
    
    # Verify webhook signature for security
    # Only verify if a real secret is configured (not the default placeholder)
    if webhook_secret and webhook_secret != 'your-webhook-secret-here':
        if not verify_webhook_signature(request.data, signature, webhook_secret):
            print("❌ Signature verification failed!")
            return jsonify({'error': 'Invalid signature'}), 401
    
    # Parse JSON payload with error handling
    try:
        payload = request.json
        if not payload:
            print("❌ No JSON payload received")
            return jsonify({'error': 'No payload'}), 400
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}")
        return jsonify({'error': 'Invalid JSON'}), 400
    
    print(f"Payload received: {event_type}")
    
    # Initialize variable to hold extracted event data
    event_data = None
    
    # Process different event types
    # Each event type has different payload structure
    
    if event_type == 'push':
        """
        Push Event Processing
        
        Triggered when commits are pushed to the repository.
        
        Payload Structure:
            {
                "ref": "refs/heads/main",        # Branch reference
                "after": "abc123...",            # Commit SHA after push
                "pusher": {
                    "name": "username",          # GitHub username
                    "email": "user@example.com"
                },
                ...
            }
        """
        event_data = {
            'request_id': payload.get('after', 'unknown'),  # Commit SHA
            'author': payload.get('pusher', {}).get('name', 'Unknown'),
            'action': 'PUSH',
            'from_branch': None,  # Push events don't have a source branch
            'to_branch': payload.get('ref', '').replace('refs/heads/', ''),  # Extract branch name
            'timestamp': datetime.utcnow().isoformat()  # Current UTC time
        }
        print(f"✅ Push event: {event_data['author']} pushed to {event_data['to_branch']}")
    
    elif event_type == 'pull_request':
        """
        Pull Request Event Processing
        
        Triggered for PR actions: opened, closed, reopened, etc.
        We handle 'opened', 'reopened' as PULL_REQUEST events
        and 'closed' with merged=true as MERGE events.
        
        Payload Structure:
            {
                "action": "opened|closed|reopened|...",
                "pull_request": {
                    "id": 123,
                    "user": {"login": "username"},
                    "head": {"ref": "feature-branch"},
                    "base": {"ref": "main"},
                    "merged": true|false,
                    "merged_by": {"login": "username"},
                    "merge_commit_sha": "abc123..."
                }
            }
        """
        # Get the specific PR action
        action = payload.get('action')
        # Extract PR details
        pr = payload.get('pull_request', {})
        
        if action == 'opened' or action == 'reopened':
            # Handle PR creation/reopening
            event_data = {
                'request_id': str(pr.get('id', 'unknown')),  # PR ID as string
                'author': pr.get('user', {}).get('login', 'Unknown'),  # PR creator
                'action': 'PULL_REQUEST',
                'from_branch': pr.get('head', {}).get('ref', 'unknown'),  # Source branch
                'to_branch': pr.get('base', {}).get('ref', 'unknown'),    # Target branch
                'timestamp': datetime.utcnow().isoformat()
            }
            print(f"✅ PR event: {event_data['author']} created PR from {event_data['from_branch']} to {event_data['to_branch']}")
        
        elif action == 'closed' and pr.get('merged'):
            # Handle PR merge (special case of closed PR where merged=true)
            event_data = {
                'request_id': pr.get('merge_commit_sha', 'unknown'),  # Merge commit SHA
                'author': pr.get('merged_by', {}).get('login', 'Unknown'),  # Who merged
                'action': 'MERGE',
                'from_branch': pr.get('head', {}).get('ref', 'unknown'),  # Source branch
                'to_branch': pr.get('base', {}).get('ref', 'unknown'),    # Target branch
                'timestamp': datetime.utcnow().isoformat()
            }
            print(f"✅ Merge event: {event_data['author']} merged {event_data['from_branch']} to {event_data['to_branch']}")
    
    # If we extracted event data, save it to MongoDB
    if event_data:
        try:
            # Insert the event document into MongoDB
            # mongo.db.events accesses the 'events' collection
            result = mongo.db.events.insert_one(event_data)
            print(f"✅ Event saved to MongoDB with ID: {result.inserted_id}")
            
            # Return success response with the created document ID
            return jsonify({
                'status': 'success',
                'id': str(result.inserted_id)  # Convert ObjectId to string
            }), 200
            
        except Exception as e:
            # Log and return database errors
            print(f"❌ Error saving to MongoDB: {e}")
            return jsonify({
                'error': 'Database error',
                'message': str(e)
            }), 500
    
    # If event_data is None, this event type is not handled
    print(f"⚠️ Event ignored: {event_type} - {payload.get('action', 'no action')}")
    return jsonify({
        'status': 'ignored',
        'reason': 'Event type not handled'
    }), 200


@webhook.route('/test', methods=['GET'])
def test():
    """
    Health check endpoint for the webhook receiver.
    
    This endpoint is useful for:
    1. Verifying the webhook service is running
    2. Testing connectivity without sending actual webhook data
    3. Monitoring/uptime checks
    
    Returns:
        JSON: Status information including current timestamp
        
    Example Response:
        {
            "status": "ok",
            "message": "Webhook endpoint is working",
            "timestamp": "2024-01-01T12:00:00.000000"
        }
    """
    return jsonify({
        'status': 'ok',
        'message': 'Webhook endpoint is working',
        'timestamp': datetime.utcnow().isoformat()  # Current UTC timestamp
    })
