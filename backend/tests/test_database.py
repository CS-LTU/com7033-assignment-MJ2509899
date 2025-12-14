"""Unit Tests for Database Operations

Tests the SQLite database functions including:
- Database initialization
- User CRUD operations
- Patient CRUD operations
- Password hashing and verification
- Data integrity
"""

import pytest
import os
import sqlite3
from backend.db.db_sql import (
    init_db, register_user, authenticate_user,
    get_all_patients, get_patient_by_id,
    add_patient, update_patient, delete_patient,
    DATABASE
)


class TestDatabaseInit:
    """Test suite for database initialization"""
    
    def test_init_db_creates_tables(self):
        """Test that init_db creates required tables"""
        init_db()
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Check users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None
        
        # Check patients table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='patients'")
        assert cursor.fetchone() is not None
        
        conn.close()
    
    def test_init_db_idempotent(self):
        """Test that init_db can be called multiple times safely"""
        init_db()
        init_db()  # Should not raise error
        
        # Tables should still exist
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        assert len(tables) >= 2  # At least users and patients tables


class TestUserOperations:
    """Test suite for user database operations"""
    
    def test_register_user_success(self):
        """Test successful user registration"""
        init_db()
        result = register_user('testuser', 'test@example.com', 'password123', 'user')
        assert result is True
    
    def test_register_duplicate_email(self):
        """Test that duplicate email is rejected"""
        init_db()
        register_user('user1', 'duplicate@example.com', 'pass1', 'user')
        result = register_user('user2', 'duplicate@example.com', 'pass2', 'user')
        assert result is False
    
    def test_register_duplicate_username(self):
        """Test that duplicate username is rejected"""
        init_db()
        register_user('duplicate_user', 'email1@example.com', 'pass1', 'user')
        result = register_user('duplicate_user', 'email2@example.com', 'pass2', 'user')
        assert result is False
    
    def test_authenticate_user_success(self):
        """Test successful user authentication"""
        init_db()
        register_user('authuser', 'auth@example.com', 'correctpass', 'doctor')
        
        user = authenticate_user('auth@example.com', 'correctpass')
        assert user is not None
        assert user['email'] == 'auth@example.com'
        assert user['role'] == 'doctor'
    
    def test_authenticate_user_wrong_password(self):
        """Test authentication fails with wrong password"""
        init_db()
        register_user('authuser2', 'auth2@example.com', 'correctpass', 'user')
        
        user = authenticate_user('auth2@example.com', 'wrongpass')
        assert user is None
    
    def test_authenticate_nonexistent_user(self):
        """Test authentication fails for non-existent user"""
        init_db()
        user = authenticate_user('nonexistent@example.com', 'anypass')
        assert user is None
    
    def test_password_hashing(self):
        """Test that passwords are hashed (not stored in plain text)"""
        init_db()
        password = 'mysecretpassword'
        register_user('hashtest', 'hash@example.com', password, 'user')
        
        # Check that stored password is not the plain text
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email='hash@example.com'")
        stored_password = cursor.fetchone()[0]
        conn.close()
        
        assert stored_password != password
        assert len(stored_password) > 50  # Bcrypt hashes are long


class TestPatientOperations:
    """Test suite for patient database operations"""
    
    @pytest.fixture
    def sample_patient_data(self):
        """Sample patient data for tests"""
        return {
            'name': 'Test Patient',
            'age': 55,
            'gender': 'Female',
            'hypertension': True,
            'heart_disease': False,
            'ever_married': 'Yes',
            'work_type': 'Self-employed',
            'residence_type': 'Rural',
            'avg_glucose_level': 125.5,
            'bmi': 30.2,
            'smoking_status': 'formerly smoked',
            'stroke_prediction': 0.45
        }
    
    def test_add_patient_returns_id(self, sample_patient_data):
        """Test that add_patient returns a patient ID"""
        init_db()
        patient_id = add_patient(sample_patient_data)
        assert isinstance(patient_id, int)
        assert patient_id > 0
    
    def test_get_patient_by_id(self, sample_patient_data):
        """Test retrieving patient by ID"""
        init_db()
        patient_id = add_patient(sample_patient_data)
        
        patient = get_patient_by_id(patient_id)
        assert patient is not None
        assert patient['name'] == sample_patient_data['name']
        assert patient['age'] == sample_patient_data['age']
    
    def test_get_all_patients(self, sample_patient_data):
        """Test retrieving all patients"""
        init_db()
        # Add multiple patients
        add_patient(sample_patient_data)
        
        second_patient = sample_patient_data.copy()
        second_patient['name'] = 'Second Patient'
        add_patient(second_patient)
        
        patients = get_all_patients()
        assert len(patients) >= 2
        assert all('name' in p for p in patients)
    
    def test_update_patient_success(self, sample_patient_data):
        """Test updating patient data"""
        init_db()
        patient_id = add_patient(sample_patient_data)
        
        # Update patient
        updated_data = sample_patient_data.copy()
        updated_data['name'] = 'Updated Name'
        updated_data['age'] = 60
        
        result = update_patient(patient_id, updated_data)
        assert result is True
        
        # Verify update
        patient = get_patient_by_id(patient_id)
        assert patient['name'] == 'Updated Name'
        assert patient['age'] == 60
    
    def test_update_nonexistent_patient(self, sample_patient_data):
        """Test updating non-existent patient returns False"""
        init_db()
        result = update_patient(99999, sample_patient_data)
        assert result is False
    
    def test_delete_patient_success(self, sample_patient_data):
        """Test deleting patient"""
        init_db()
        patient_id = add_patient(sample_patient_data)
        
        result = delete_patient(patient_id)
        assert result is True
        
        # Verify deletion
        patient = get_patient_by_id(patient_id)
        assert patient is None
    
    def test_delete_nonexistent_patient(self):
        """Test deleting non-existent patient returns False"""
        init_db()
        result = delete_patient(99999)
        assert result is False
    
    def test_patient_timestamps(self, sample_patient_data):
        """Test that timestamps are automatically set"""
        init_db()
        patient_id = add_patient(sample_patient_data)
        
        patient = get_patient_by_id(patient_id)
        assert 'created_at' in patient
        assert 'updated_at' in patient
        assert patient['created_at'] is not None


class TestDataIntegrity:
    """Test suite for data integrity and constraints"""
    
    def test_user_email_unique(self):
        """Test that email uniqueness is enforced"""
        init_db()
        register_user('user1', 'unique@test.com', 'pass1', 'user')
        result = register_user('user2', 'unique@test.com', 'pass2', 'user')
        assert result is False
    
    def test_patient_id_autoincrement(self):
        """Test that patient IDs auto-increment"""
        init_db()
        patient1_data = {
            'name': 'Patient 1',
            'age': 40,
            'gender': 'Male',
            'hypertension': False,
            'heart_disease': False,
            'ever_married': 'No',
            'work_type': 'Private',
            'residence_type': 'Urban',
            'avg_glucose_level': 100.0,
            'bmi': 25.0,
            'smoking_status': 'never smoked',
            'stroke_prediction': 0.1
        }
        
        id1 = add_patient(patient1_data)
        
        patient2_data = patient1_data.copy()
        patient2_data['name'] = 'Patient 2'
        id2 = add_patient(patient2_data)
        
        assert id2 > id1
