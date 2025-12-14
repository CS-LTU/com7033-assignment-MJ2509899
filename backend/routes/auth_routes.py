"""Authentication Routes for NeuroGuard Healthcare System

This module provides API endpoints for user authentication including:
- User registration with role assignment (user/doctor/admin)
- User login with JWT token generation
- Password verification and validation

All routes are prefixed with /api/auth
Security features include bcrypt password hashing and JWT token authentication.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from db.db_sql import register_user, authenticate_user
import logging

# Set up logger for authentication operations
logger = logging.getLogger(__name__)

# Create authentication blueprint with /api/auth prefix
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# ==================== User Registration ====================
@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account
    
    Expected JSON body:
        {
            "username": str,
            "email": str,
            "password": str,
            "role": str (optional, defaults to 'user')
        }
    
    Returns:
        201: Success with JWT token and user data
        400: Invalid role or user already exists
    
    Roles:
        - 'user': Can view patient data only
        - 'doctor': Full CRUD access to patient records
        - 'admin': Administrative access
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default to 'user' role if not specified

    # Validate that role is one of the allowed values
    if role not in ['user', 'doctor', 'admin']:
        return jsonify({"error": "Invalid role"}), 400

    # Attempt to register the user (password will be hashed in db_sql.py)
    success = register_user(username, email, password, role)
    if success:
        logger.info(f"User registered: {email} as {role}")
        # Create user object without password for response
        user = {"username": username, "email": email, "role": role}
        # Generate JWT access token using email as identity
        token = create_access_token(identity=email)
        return jsonify({"token": token, "user": user}), 201

    # Registration failed - user already exists (duplicate email/username)
    logger.warning(f"Failed registration attempt: {email}")
    return jsonify({"error": "User already exists"}), 400

# ==================== User Login ====================
@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and generate JWT token
    
    Expected JSON body:
        {
            "email": str,
            "password": str
        }
    
    Returns:
        200: Success with JWT token and user data
        401: Invalid credentials
    
    Security:
        - Password verification uses bcrypt
        - JWT token expires based on app configuration
        - User data returned without password field
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Authenticate user (verifies password hash)
    user = authenticate_user(email, password)
    if user:
        # Generate JWT token for authenticated user
        token = create_access_token(identity=email)
        logger.info(f"User logged in: {email}")
        return jsonify({"token": token, "user": user}), 200

    # Authentication failed - invalid email or password
    logger.warning(f"Failed login attempt: {email}")
    return jsonify({"error": "Invalid credentials"}), 401
