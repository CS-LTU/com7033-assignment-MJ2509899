"""Unit Tests for Authentication Routes

Tests the authentication endpoints including:
- User registration with various roles
- User login with valid/invalid credentials
- Token generation and validation
- Error handling for duplicate users
"""

import pytest
import json
from backend.app import app
from backend.db.db_sql import init_db, get_db

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    # Initialize test database
    with app.app_context():
        init_db()
    
    with app.test_client() as client:
        yield client
    
    # Cleanup: remove test users after tests
    # In a real scenario, you'd use a separate test database

@pytest.fixture
def test_user():
    """Sample user data for testing"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'role': 'user'
    }

@pytest.fixture
def test_doctor():
    """Sample doctor data for testing"""
    return {
        'username': 'testdoctor',
        'email': 'doctor@example.com',
        'password': 'doctorpass123',
        'role': 'doctor'
    }


class TestAuthRegistration:
    """Test suite for user registration"""
    
    def test_register_user_success(self, client, test_user):
        """Test successful user registration"""
        response = client.post(
            '/api/auth/register',
            data=json.dumps(test_user),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == test_user['email']
        assert data['user']['role'] == 'user'
    
    def test_register_doctor_success(self, client, test_doctor):
        """Test successful doctor registration"""
        response = client.post(
            '/api/auth/register',
            data=json.dumps(test_doctor),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['user']['role'] == 'doctor'
    
    def test_register_invalid_role(self, client):
        """Test registration with invalid role"""
        invalid_user = {
            'username': 'invaliduser',
            'email': 'invalid@example.com',
            'password': 'password123',
            'role': 'invalid_role'
        }
        
        response = client.post(
            '/api/auth/register',
            data=json.dumps(invalid_user),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            '/api/auth/register',
            data=json.dumps(test_user),
            content_type='application/json'
        )
        
        # Attempt duplicate registration
        response = client.post(
            '/api/auth/register',
            data=json.dumps(test_user),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestAuthLogin:
    """Test suite for user login"""
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        # Register user first
        client.post(
            '/api/auth/register',
            data=json.dumps(test_user),
            content_type='application/json'
        )
        
        # Attempt login
        login_data = {
            'email': test_user['email'],
            'password': test_user['password']
        }
        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert 'user' in data
        assert data['user']['email'] == test_user['email']
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password"""
        # Register user first
        client.post(
            '/api/auth/register',
            data=json.dumps(test_user),
            content_type='application/json'
        )
        
        # Attempt login with wrong password
        login_data = {
            'email': test_user['email'],
            'password': 'wrongpassword'
        }
        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data


class TestTokenGeneration:
    """Test suite for JWT token functionality"""
    
    def test_token_format(self, client, test_user):
        """Test that generated token is in correct format"""
        response = client.post(
            '/api/auth/register',
            data=json.dumps(test_user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        token = data['token']
        
        # JWT tokens have 3 parts separated by dots
        assert token.count('.') == 2
        assert len(token) > 50  # JWT tokens are typically long
