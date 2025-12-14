"""SQLite Database Operations for NeuroGuard Healthcare System

This module handles all SQLite database operations including:
- User authentication and registration
- Patient CRUD operations
- Database initialization and schema management

The database uses SQLite for lightweight, fast local operations with
automatic schema creation and data persistence.

Database Schema:
- users: Stores user credentials and roles (user/doctor)
- patients: Stores patient health records and stroke predictions
"""

import sqlite3
import os
from flask_bcrypt import Bcrypt

# Initialize Bcrypt instance for password hashing
bcrypt = Bcrypt()

# Database Configuration
# Use absolute path to ensure consistent database location across different working directories
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(DB_DIR, '..', 'users.db')

def get_db():
    """Create and return a database connection with Row factory
    
    Returns:
        sqlite3.Connection: Database connection with row factory for dict-like access
    """
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Enables column access by name
    return db

def init_db():
    """Initialize the SQLite database with users and patients tables
    
    Creates two tables if they don't exist:
    1. users: For authentication and role-based access control
    2. patients: For storing patient health records
    
    The function is idempotent - safe to call multiple times.
    """
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('user','doctor')) NOT NULL
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                hypertension BOOLEAN NOT NULL,
                heart_disease BOOLEAN NOT NULL,
                ever_married TEXT NOT NULL,
                work_type TEXT NOT NULL,
                residence_type TEXT NOT NULL,
                avg_glucose_level REAL NOT NULL,
                bmi REAL NOT NULL,
                smoking_status TEXT NOT NULL,
                stroke_prediction REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

def register_user(username, email, password, role):
    """Register a new user with hashed password
    
    Args:
        username (str): Unique username for the user
        email (str): Unique email address
        password (str): Plain text password (will be hashed)
        role (str): User role - 'user' or 'doctor'
    
    Returns:
        bool: True if registration successful, False if user already exists
    
    Security:
        - Passwords are hashed using bcrypt before storage
        - Email and username must be unique (enforced by database constraints)
    """
    # Hash the password using bcrypt with automatic salt generation
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        with get_db() as db:
            db.execute(
                "INSERT INTO users (username,email,password,role) VALUES (?,?,?,?)",
                (username, email, hashed_password, role)
            )
            db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(email, password):
    """Authenticate user by email and password
    
    Args:
        email (str): User's email address
        password (str): Plain text password to verify
    
    Returns:
        dict: User data (id, username, email, role) if authenticated
        None: If authentication fails
    
    Security:
        - Uses bcrypt to verify password against stored hash
        - Returns user data without password field
    """
    with get_db() as db:
        user = db.execute(
            "SELECT id, username, email, role, password FROM users WHERE email=?",
            (email,)
        ).fetchone()
        if user and bcrypt.check_password_hash(user['password'], password):
            return {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
    return None

# ==================== Patient CRUD Operations ====================
# Functions for managing patient health records in the database

def get_all_patients():
    """Fetch all patients from the database
    
    Returns:
        list[dict]: List of all patient records as dictionaries
    """
    with get_db() as db:
        patients = db.execute("SELECT * FROM patients").fetchall()
        return [dict(p) for p in patients]

def get_patient_by_id(patient_id):
    """Fetch a single patient by ID
    
    Args:
        patient_id (int): The unique patient identifier
    
    Returns:
        dict: Patient record if found, None otherwise
    """
    with get_db() as db:
        patient = db.execute("SELECT * FROM patients WHERE id=?", (patient_id,)).fetchone()
        return dict(patient) if patient else None

def add_patient(data):
    """Add a new patient to the database
    
    Args:
        data (dict): Patient data including all required fields:
            - name, age, gender
            - hypertension, heart_disease (boolean)
            - ever_married, work_type, residence_type
            - avg_glucose_level, bmi
            - smoking_status, stroke_prediction
    
    Returns:
        int: The ID of the newly created patient record
    """
    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO patients (name, age, gender, hypertension, heart_disease, ever_married, 
                                work_type, residence_type, avg_glucose_level, bmi, smoking_status, stroke_prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['name'], data['age'], data['gender'], data['hypertension'], data['heart_disease'],
            data['ever_married'], data['work_type'], data['residence_type'], data['avg_glucose_level'],
            data['bmi'], data['smoking_status'], data.get('stroke_prediction')
        ))
        db.commit()
        return cursor.lastrowid

def update_patient(patient_id, data):
    """Update an existing patient record
    
    Args:
        patient_id (int): The unique patient identifier
        data (dict): Updated patient data (same fields as add_patient)
    
    Returns:
        bool: True if update successful, False if patient not found
    
    Note:
        Automatically updates the 'updated_at' timestamp
    """
    with get_db() as db:
        db.execute("""
            UPDATE patients SET name=?, age=?, gender=?, hypertension=?, heart_disease=?, ever_married=?, 
                              work_type=?, residence_type=?, avg_glucose_level=?, bmi=?, smoking_status=?, 
                              stroke_prediction=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (
            data['name'], data['age'], data['gender'], data['hypertension'], data['heart_disease'],
            data['ever_married'], data['work_type'], data['residence_type'], data['avg_glucose_level'],
            data['bmi'], data['smoking_status'], data.get('stroke_prediction'), patient_id
        ))
        db.commit()
        return db.total_changes > 0

def delete_patient(patient_id):
    """Delete a patient record by ID
    
    Args:
        patient_id (int): The unique patient identifier
    
    Returns:
        bool: True if deletion successful, False if patient not found
    
    Warning:
        This operation is permanent and cannot be undone
    """
    with get_db() as db:
        db.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        db.commit()
        return db.total_changes > 0
