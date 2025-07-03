"""
Flask Application Factory
========================
This module contains the application factory function that creates and configures
the Flask application. Using the factory pattern allows for easy testing and
multiple configurations.

The create_app function:
1. Creates the Flask instance
2. Loads configuration
3. Initializes extensions
4. Registers blueprints
5. Defines routes
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from app.extensions import mongo
from app.webhook.routes import webhook


def create_app():
    """
    Application factory function that creates and configures the Flask app.
    
    This function follows the Flask application factory pattern, which allows
    for better testing, multiple configurations, and cleaner code organization.
    
    Returns:
        Flask: Configured Flask application instance ready to run
    
    Configuration:
        Loads from config.Config class which should contain:
        - SECRET_KEY: Flask secret key for sessions
        - MONGO_URI: MongoDB connection string
        - WEBHOOK_SECRET: GitHub webhook verification secret
    """
    
    # Create Flask application instance
    # __name__ helps Flask locate resources relative to this module
    app = Flask(__name__)
    
    # Load configuration from config.py Config class
    # This sets app.config with all the configuration variables
    # The string 'config.Config' tells Flask to:
    # 1. Import the 'config' module
    # 2. Get the 'Config' class from it
    # 3. Load all UPPERCASE attributes as config values
    app.config.from_object('config.Config')
    
    # Initialize MongoDB extension with this app instance
    # This establishes the database connection using app.config['MONGO_URI']
    mongo.init_app(app)
    
    # Initialize CORS (Cross-Origin Resource Sharing)
    # This allows the API to be called from different domains
    # Useful when frontend and backend are on different servers
    CORS(app)
    
    # Register the webhook blueprint
    # Blueprints allow us to organize routes into modules
    # The webhook blueprint handles all /webhook/* routes
    app.register_blueprint(webhook)
    
    # Define the main route that serves the UI
    @app.route('/')
    def index():
        """
        Serve the main UI page.
        
        This route renders the index.html template which contains
        the JavaScript application that polls for updates.
        
        Returns:
            str: Rendered HTML template
        """
        return render_template('index.html')
    
    # Define API endpoint for retrieving events
    @app.route('/api/events', methods=['GET'])
    def get_events():
        """
        API endpoint to retrieve the latest GitHub events.
        
        This endpoint is called by the frontend every 15 seconds to get
        the latest events from the database. It returns events in reverse
        chronological order (newest first).
        
        Returns:
            JSON: Array of event objects, limited to 10 most recent
            
        Response Format:
            [
                {
                    "_id": "507f1f77bcf86cd799439011",
                    "request_id": "abc123",
                    "author": "username",
                    "action": "PUSH|PULL_REQUEST|MERGE",
                    "from_branch": "feature",
                    "to_branch": "main",
                    "timestamp": "2024-01-01T12:00:00.000000"
                }
            ]
        """
        # Query MongoDB for events
        # .find() - gets all documents from 'events' collection
        # .sort('timestamp', -1) - sorts by timestamp descending (newest first)
        # .limit(10) - limits results to 10 documents
        # list() - converts cursor to list for easier manipulation
        events = list(mongo.db.events.find().sort('timestamp', -1).limit(10))
        
        # MongoDB's ObjectId is not JSON serializable by default
        # We need to convert it to string for the JSON response
        for event in events:
            event['_id'] = str(event['_id'])
        
        # Return events as JSON with proper content-type headers
        return jsonify(events)
    
    # Return the configured app instance
    return app
