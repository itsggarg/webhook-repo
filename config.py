"""
Application Configuration Module
================================
This module handles all configuration settings for the Flask application.
It uses environment variables for sensitive data and provides sensible defaults
for development. The configuration follows the principle of "explicit is better
than implicit" and separates concerns between different environments.

Configuration Management:
    - Uses python-dotenv to load environment variables from .env file
    - Provides default values for development
    - Keeps sensitive data out of source code
    - Makes it easy to switch between development/production settings

Environment Variables Expected:
    SECRET_KEY: Flask secret key for session encryption
    MONGO_URI: MongoDB connection string with credentials
    WEBHOOK_SECRET: GitHub webhook verification secret
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Example .env file:
# SECRET_KEY=your-super-secret-key-here
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
# WEBHOOK_SECRET=github-webhook-secret
load_dotenv()


class Config:
    """
    Configuration class for Flask application.
    """
    
    # Flask SECRET_KEY Configuration
    # ==============================
    # This key is used by Flask for:
    # - Signing session cookies
    # - CSRF protection
    # - Any cryptographic operations
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # MongoDB Connection Configuration
    # ================================
    # MongoDB URI format:
    # - Atlas: mongodb+srv://username:password@cluster.mongodb.net/database_name
    #
    # The URI contains:
    # - Protocol: mongodb:// or mongodb+srv:// (for Atlas)
    # - Credentials: username:password (if auth enabled)
    # - Host(s): localhost:27017 or cluster.mongodb.net
    # - Database: /database_name (optional, can be specified later)
    # - Options: ?retryWrites=true&w=majority (connection options)
    #
    # Flask-PyMongo expects this to be named exactly 'MONGO_URI'
    # The extension looks for app.config['MONGO_URI'] during initialization
    MONGO_URI = os.environ.get('MONGO_URI')
    
    # GitHub Webhook Secret Configuration
    # ===================================
    # This secret is used to verify that webhooks are actually from GitHub
    # 
    # How it works:
    # 1. You configure this secret in GitHub webhook settings
    # 2. GitHub uses it to create HMAC-SHA256 signature of payload
    # 3. We verify the signature to ensure webhook authenticity
    
    WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')
    
    
