"""Flask Application Entry Point for NeuroGuard Healthcare System

This module initializes the Flask application with dual database support
(MongoDB and SQLite), configures JWT authentication, sets up CORS for
frontend communication, and registers API route blueprints.

Key Features:
- JWT-based authentication with bcrypt password hashing
- Dual database architecture (MongoDB + SQLite)
- Request/Response logging middleware
- CORS configuration for multiple frontend origins
- RESTful API endpoints for authentication and patient management
"""

import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Database imports - both MongoDB and SQLite for dual database architecture
from db.db_mongo import connect_mongo
from db.db_sql import init_db

# Route blueprints for modular API endpoints
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp

# Load environment variables from .env file for secure configuration
load_dotenv()

# ==================== Flask Application Setup ====================
app = Flask(__name__)

# Configure CORS to allow requests from frontend development servers
# Supports credentials for JWT token-based authentication
CORS(app, origins=[
    "http://localhost:3000",  # Primary Vite dev server
    "http://localhost:3001",  # Alternate port
    "http://localhost:3002"   # Alternate port
], supports_credentials=True)

# ==================== Configuration ====================
# JWT secret key for token signing and verification
app.config["JWT_SECRET_KEY"] = "super-secret-key"

# MongoDB Atlas connection string for cloud database
# Used for scalable patient data storage in production
app.config["MONGO_URI"] = (
    "mongodb+srv://muzamilhabib529_db_user:mxTfQZU8gpXce3QQ@cluster1.sv5zxbm.mongodb.net/healthcare_db?retryWrites=true&w=majority"
)

# ==================== Initialize Extensions ====================
CORS(app)  # Enable CORS for all routes
JWTManager(app)  # Initialize JWT authentication manager
connect_mongo()  # Establish MongoDB connection


# ================= ROUTES =================



# ==================== Request/Response Logging Middleware ====================
# Logs all incoming requests and outgoing responses for debugging and monitoring

@app.before_request
def log_request_info():
    """Log incoming request details including method, URL, headers, and body"""
    from flask import request
    logger.info('=' * 50)
    logger.info(f'REQUEST: {request.method} {request.url}')
    logger.info(f'Headers: {dict(request.headers)}')
    if request.data:
        logger.info(f'Body: {request.get_data(as_text=True)}')
    logger.info('=' * 50)

@app.after_request
def log_response_info(response):
    """Log response status code for each request"""
    logger.info(f'RESPONSE: {response.status}')
    return response

# ==================== Security Configuration ====================
# Configure JWT secret key from environment variable with fallback
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
jwt = JWTManager(app)

# Initialize Bcrypt for secure password hashing (using bcrypt algorithm)
bcrypt = Bcrypt(app)

# ==================== Logging Configuration ====================
# Set up application-wide logging with INFO level for production monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting Flask app...")

# ==================== Database Initialization ====================
# Initialize SQLite database for primary operations (authentication & patient data)
# SQLite is used for fast local operations and development
init_db()
logger.info("SQLite database initialized.")

# MongoDB is connected but not actively used - ready for cloud migration
# Both databases are initialized to support future data migration strategies
# MongoDB can be enabled for production scalability when needed

# ==================== Register API Blueprints ====================
# Register authentication routes (/api/auth/register, /api/auth/login)
app.register_blueprint(auth_bp)
logger.info("Auth blueprint registered.")

# Register patient management routes (GET, POST, PUT, DELETE /api/patients)
app.register_blueprint(patient_bp)
logger.info("Patient blueprint registered.")

# ----- Run Flask App -----
if __name__ == '__main__':
    logger.info("Flask app running on http://localhost:5000")
    app.run(debug=True, port=5000)
