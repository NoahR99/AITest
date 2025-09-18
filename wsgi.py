"""WSGI entry point for production deployment."""

import os
from web_app import app

# Ensure directories exist
from config import OUTPUT_DIR, TEMP_DIR
OUTPUT_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Production configuration
if os.getenv('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'ai-generator-production-key-change-this')

if __name__ == "__main__":
    app.run()