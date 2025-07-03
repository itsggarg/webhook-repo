"""
MongoDB Extension Module
=======================
This module provides a custom MongoDB wrapper class that integrates with Flask applications.
It follows the Flask extension pattern, allowing for clean initialization and configuration.

The MongoDB class manages the database connection and provides easy access to the database
instance throughout the application.
"""

from pymongo import MongoClient
import os


class MongoDB:
    """
    Custom MongoDB wrapper for Flask applications.
    
    This class provides a clean interface for initializing and accessing MongoDB
    within a Flask application context. It follows the Flask extension pattern
    with an init_app method for deferred initialization.
    
    Attributes:
        client (MongoClient): The MongoDB client instance used for database connections
        db (Database): The specific database instance for our application
    
    Usage:
        # In extensions.py
        mongo = MongoDB()
        
        # In app factory
        mongo.init_app(app)
        
        # Accessing the database
        mongo.db.collection_name.find()
    """
    
    def __init__(self):
        """
        Initialize the MongoDB extension.
        
        The actual connection is not established here - it's deferred until
        init_app() is called. This allows the extension to be initialized
        without an app instance, following the Flask application factory pattern.
        """
        self.client = None  # Will hold the MongoClient instance
        self.db = None      # Will hold the specific database instance
    
    def init_app(self, app):
        """
        Initialize the MongoDB connection with the Flask application.
        
        This method is called during app creation to establish the database
        connection using configuration from the Flask app.
        
        Args:
            app (Flask): The Flask application instance containing configuration
        
        Configuration Expected:
            MONGO_URI: The MongoDB connection string (required)
                      Format: mongodb+srv://username:password@cluster.mongodb.net/
        
        Note:
            Currently hardcoded to use 'github_webhooks' database.
            TODO: Make database name configurable via app.config
        """
        # Retrieve MongoDB URI from Flask configuration
        # This should be set in config.py or environment variables
        mongo_uri = app.config.get('MONGO_URI')
        
        # Create MongoDB client with the connection string
        # This establishes the connection pool but doesn't actually connect yet
        # MongoDB uses lazy connection - it connects when first operation is performed
        self.client = MongoClient(mongo_uri)
        
        # Select the specific database we'll be using
        # TODO: Extract database name from URI or make it configurable
        # Current implementation uses hardcoded database name
        db_name = 'github_webhooks'
        
        # Get reference to our database
        # This doesn't create the database - MongoDB creates it on first write
        self.db = self.client[db_name]


# Create a singleton instance of MongoDB extension
# This instance will be imported and used throughout the application
# Following the Flask extension pattern for easy integration
mongo = MongoDB()
