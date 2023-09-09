# Import necessary modules and libraries
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()

# Create a Flask application factory function
def create_app(script_info=None):
    # Instantiate the Flask app
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing (CORS) for the app
    cors = CORS(app)

    # Load configuration settings from the environment variable APP_SETTINGS
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    
    # Configure CORS headers for the app
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initialize database extension for the app
    db.init_app(app)

    # Initialize database migration extension for the app
    migrate.init_app(app, db)

    # Register blueprints (routes) for the app
    from .views.views import views
    from .api.api import api

    app.register_blueprint(views)
    app.register_blueprint(api)

    # Define error handlers for specific HTTP status codes
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "status": "error",
            "error": e.description
        }), 400

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({
            "status": "error",
            "error": e.description
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "status": "error",
            "error": "This wasn't supposed to happen"
        })

    # Define a shell context for Flask CLI
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    
    return app
