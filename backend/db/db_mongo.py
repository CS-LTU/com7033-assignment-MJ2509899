"""MongoDB Database Operations for NeuroGuard Healthcare System

This module handles all MongoDB Atlas operations including:
- Connection to MongoDB Atlas cloud database
- Patient CRUD operations using MongoDB
- Bulk data upload from CSV files
- Document-based data storage for scalability
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import logging

logger = logging.getLogger(__name__)

client = None
db = None

def connect_mongo():
    """Connect to MongoDB Atlas cloud database
    
    Establishes connection to MongoDB cluster and selects healthcare database.
    Connection URI includes authentication and retry settings.
    """
    global client, db

    MONGO_URI = (
        "mongodb+srv://muzamilhabib529_db_user:mxTfQZU8gpXce3QQ@cluster1.sv5zxbm.mongodb.net/"
        "healthcare_db?retryWrites=true&w=majority"
    )

    try:
        client = MongoClient(MONGO_URI)
        db = client["healthcare_db"]  # Database name
        # Test connection
        client.server_info()
        logger.info("MongoDB Atlas connected successfully")
        print("✅ MongoDB Atlas connected")
    except Exception as e:
        logger.error(f"MongoDB connection failed: {e}")
        print(f"❌ MongoDB connection failed: {e}")
        client = None

def get_patients_collection():
    """Get the patients collection from MongoDB
    
    Returns:
        Collection: MongoDB patients collection
    
    Raises:
        Exception: If MongoDB is not connected
    """
    if client is None:
        raise Exception("MongoDB not connected")
    return db["patients"]

# ==================== MongoDB CRUD Operations ====================

def get_all_patients_mongo():
    """Fetch all patient records from MongoDB
    
    Returns:
        list[dict]: List of all patient documents with _id converted to string
    """
    try:
        collection = get_patients_collection()
        patients = list(collection.find())
        # Convert ObjectId to string for JSON serialization
        for patient in patients:
            patient['_id'] = str(patient['_id'])
        logger.info(f"Fetched {len(patients)} patients from MongoDB")
        return patients
    except Exception as e:
        logger.error(f"Error fetching patients from MongoDB: {e}")
        return []

def get_patient_by_id_mongo(patient_id):
    """Fetch a single patient by MongoDB ObjectId
    
    Args:
        patient_id (str): MongoDB ObjectId as string
    
    Returns:
        dict: Patient document or None if not found
    """
    try:
        collection = get_patients_collection()
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient['_id'] = str(patient['_id'])
        return patient
    except Exception as e:
        logger.error(f"Error fetching patient {patient_id}: {e}")
        return None

def add_patient_mongo(data):
    """Add a new patient to MongoDB
    
    Args:
        data (dict): Patient data including all health fields
    
    Returns:
        str: The inserted patient's ObjectId as string
    """
    try:
        collection = get_patients_collection()
        result = collection.insert_one(data)
        logger.info(f"Added patient to MongoDB: {data.get('name')}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error adding patient to MongoDB: {e}")
        raise

def update_patient_mongo(patient_id, data):
    """Update an existing patient in MongoDB
    
    Args:
        patient_id (str): MongoDB ObjectId as string
        data (dict): Updated patient data
    
    Returns:
        bool: True if update successful, False otherwise
    """
    try:
        collection = get_patients_collection()
        result = collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": data}
        )
        logger.info(f"Updated patient {patient_id} in MongoDB")
        return result.modified_count > 0
    except Exception as e:
        logger.error(f"Error updating patient {patient_id}: {e}")
        return False

def delete_patient_mongo(patient_id):
    """Delete a patient from MongoDB
    
    Args:
        patient_id (str): MongoDB ObjectId as string
    
    Returns:
        bool: True if deletion successful, False otherwise
    """
    try:
        collection = get_patients_collection()
        result = collection.delete_one({"_id": ObjectId(patient_id)})
        logger.info(f"Deleted patient {patient_id} from MongoDB")
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Error deleting patient {patient_id}: {e}")
        return False

def bulk_insert_patients_mongo(patients_data):
    """Bulk insert multiple patients into MongoDB
    
    Args:
        patients_data (list[dict]): List of patient documents to insert
    
    Returns:
        int: Number of documents inserted
    """
    try:
        collection = get_patients_collection()
        result = collection.insert_many(patients_data)
        count = len(result.inserted_ids)
        logger.info(f"Bulk inserted {count} patients to MongoDB")
        return count
    except Exception as e:
        logger.error(f"Error bulk inserting patients: {e}")
        return 0

def count_patients_mongo():
    """Get total count of patients in MongoDB
    
    Returns:
        int: Number of patient documents
    """
    try:
        collection = get_patients_collection()
        return collection.count_documents({})
    except Exception as e:
        logger.error(f"Error counting patients: {e}")
        return 0

def clear_all_patients_mongo():
    """Delete all patients from MongoDB (use with caution!)
    
    Returns:
        int: Number of documents deleted
    """
    try:
        collection = get_patients_collection()
        result = collection.delete_many({})
        logger.warning(f"Cleared {result.deleted_count} patients from MongoDB")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Error clearing patients: {e}")
        return 0
