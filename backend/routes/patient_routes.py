"""Patient Management Routes for NeuroGuard Healthcare System

This module provides RESTful API endpoints for patient data management:
- GET /api/patients/ - Retrieve all patients
- POST /api/patients/ - Add new patient (Doctor only)
- PUT /api/patients/<id> - Update patient (Doctor only)
- DELETE /api/patients/<id> - Delete patient (Doctor only)

✅ NOW USING MONGODB for all patient operations!
JWT authentication is configured but temporarily disabled for testing.

Role-based Access:
- Users: Can view patient data (GET)
- Doctors: Full CRUD access
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
# MongoDB imports - ACTIVE!
from bson.objectid import ObjectId
from db.db_mongo import (
    get_all_patients_mongo,
    get_patient_by_id_mongo,
    add_patient_mongo,
    update_patient_mongo,
    delete_patient_mongo
)
import logging

# Set up logger for patient operations
logger = logging.getLogger(__name__)

# Create patient blueprint with /api/patients prefix
patient_bp = Blueprint('patients', __name__, url_prefix='/api/patients')

# ==================== Get All Patients ====================
@patient_bp.route('/', methods=['GET'])
# @jwt_required(optional=True)  # Temporarily disabled for testing
def get_patients():
    """Retrieve all patient records from MongoDB
    
    Returns:
        200: JSON array of all patient records
        500: Server error with error message
    
    Access: All authenticated users (read-only for 'user' role)
    """
    try:
        # Fetch all patients from MongoDB
        patients = get_all_patients_mongo()
        logger.info(f"Fetched {len(patients)} patients from MongoDB")
        return jsonify(patients), 200
    except Exception as e:
        logger.error(f"Error fetching patients from MongoDB: {e}")
        return jsonify({"error": str(e)}), 500

# ==================== Add New Patient ====================
@patient_bp.route('/', methods=['POST'])
# @jwt_required(optional=True)
def add_patient_route():
    """Add a new patient record to MongoDB
    
    Expected JSON body includes:
        name, age, gender, hypertension, heart_disease,
        ever_married, work_type, residence_type,
        avg_glucose_level, bmi, smoking_status, stroke
    
    Returns:
        201: Newly created patient record with MongoDB _id
        400: Bad request with error message
    
    Access: Doctors only (role-based restriction to be enforced)
    """
    try:
        data = request.json
        # Add patient to MongoDB and get the new ObjectId
        patient_id = add_patient_mongo(data)
        # Fetch the complete patient record to return
        patient_data = get_patient_by_id_mongo(patient_id)
        logger.info(f"Added new patient to MongoDB: {data.get('name')}")
        return jsonify(patient_data), 201
    except Exception as e:
        logger.error(f"Error adding patient to MongoDB: {e}")
        return jsonify({"error": str(e)}), 400

# ==================== Update Patient ====================
@patient_bp.route('/<string:id>', methods=['PUT'])
# @jwt_required(optional=True)
def update_patient_route(id):
    """Update an existing patient record in MongoDB
    
    Args:
        id (str): MongoDB ObjectId as string from URL path
    
    Expected JSON body: Same fields as add_patient
    
    Returns:
        200: Updated patient record
        404: Patient not found
        400: Bad request with error message
    
    Access: Doctors only (role-based restriction to be enforced)
    """
    try:
        data = request.json
        # Attempt to update the patient record in MongoDB
        success = update_patient_mongo(id, data)
        if not success:
            logger.warning(f"Patient not found for update: {id}")
            return jsonify({"error": "Patient not found"}), 404
        
        # Fetch updated patient data to return
        patient_data = get_patient_by_id_mongo(id)
        logger.info(f"Updated patient in MongoDB: {id}")
        return jsonify(patient_data), 200
    except Exception as e:
        logger.error(f"Error updating patient {id}: {e}")
        return jsonify({"error": str(e)}), 400

# ==================== Delete Patient ====================
@patient_bp.route('/<string:id>', methods=['DELETE'])
# @jwt_required(optional=True)
def delete_patient_route(id):
    """Delete a patient record from MongoDB
    
    Args:
        id (str): MongoDB ObjectId as string from URL path
    
    Returns:
        200: Success message
        404: Patient not found
        500: Server error with error message
    
    Access: Doctors only (role-based restriction to be enforced)
    Warning: This operation is permanent and cannot be undone
    """
    try:
        # Attempt to delete the patient record from MongoDB
        success = delete_patient_mongo(id)
        if not success:
            logger.warning(f"Patient not found for deletion: {id}")
            return jsonify({"error": "Patient not found"}), 404
        
        logger.info(f"Deleted patient from MongoDB: {id}")
        return jsonify({"message": "Patient deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting patient {id}: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error deleting patient {id}: {e}")
        return jsonify({"error": str(e)}), 500

