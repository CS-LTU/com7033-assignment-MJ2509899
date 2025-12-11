import json
import sqlite3
from flask import Flask, jsonify, request, send_from_directory
from bson.objectid import ObjectId
from pymongo import MongoClient

# --- Configuration ---
app = Flask(__name__, static_folder='static')

# Database file paths
LOGIN_DB = 'login.db'
MONGO_URI = 'mongodb://localhost:27017/' # Connects to local MongoDB instance
DB_NAME = 'hms_db'
COLLECTION_NAME = 'patients'

# Define API permissions
PERMISSIONS = {
    'administrator': {'read': True, 'create': True, 'update': True, 'delete': True},
    'doctor': {'read': True, 'create': True, 'update': False, 'delete': False},
    'viewer': {'read': True, 'create': False, 'update': False, 'delete': False},
}


# --- Database Connection Utilities ---

def get_db_conn():
    """Connects to the SQLite login database."""
    conn = sqlite3.connect(LOGIN_DB)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def get_mongo_collection():
    """Connects to MongoDB and returns the patients collection."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        # In a real app, this should raise a proper error
        return None 


# --- Utility Functions ---

def generate_patient_id(patients):
    """Generates a new unique Patient ID (simple increment based on count)."""
    # NOTE: MongoDB documents already have a unique _id. 
    # This function is used to generate a user-facing ID (Pxxxx).
    if not patients:
        return 'P00001'
    
    # Simple count for a mock Pxxxx ID
    count = patients.count_documents({})
    new_number = count + 1
    return f'P{new_number:05d}'

def check_permission(role, action):
    """Checks if a given role has permission for the action."""
    return PERMISSIONS.get(role, {}).get(action, False)


# --- Core Routes ---

@app.route('/')
def serve_index():
    """Serves the main HTML file."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login', methods=['POST'])
def login():
    """Handles user authentication using SQLite."""
    data = request.json
    user_id = data.get('userId')
    password = data.get('password')

    conn = get_db_conn()
    cursor = conn.cursor()
    
    # Query SQLite database for user
    cursor.execute('SELECT password, role FROM users WHERE id = ?', (user_id,))
    user_record = cursor.fetchone()
    conn.close()

    if user_record and user_record['password'] == password:
        # Success: return the role
        return jsonify({'message': 'Login successful', 'role': user_record['role']}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401


# --- API Routes for Patient CRUD (MongoDB) ---

@app.route('/api/patients', methods=['GET'])
def get_patients():
    """READ: Returns all patient data from MongoDB."""
    
    # In a production app, the role would be retrieved from a session/JWT.
    # Here, we trust the front-end for the initial check.
    role = request.args.get('role', 'viewer') # Get role from query param 

    if not check_permission(role, 'read'):
        return jsonify({'message': 'Permission Denied: Cannot view records'}), 403

    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'message': 'Database connection failed'}), 500
        
    # Fetch all documents, convert _id to string for JSON serialization
    patients = []
    for doc in collection.find():
        doc['_id'] = str(doc['_id'])
        patients.append(doc)
        
    return jsonify(patients)

@app.route('/api/patients', methods=['POST'])
def add_patient():
    """CREATE: Adds a new patient record to MongoDB."""
    data = request.json
    role = data.pop('role', 'viewer')
    
    if not check_permission(role, 'create'):
        return jsonify({'message': 'Permission Denied: Cannot create records'}), 403

    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'message': 'Database connection failed'}), 500
        
    # Generate user-facing ID and add the record
    data['id'] = collection.find_one(sort=[('_id', -1)]).get('id', 'P00000') if collection.count_documents({}) > 0 else 'P00000'
    last_number = int(data['id'].replace('P', ''))
    data['id'] = f'P{last_number + 1:05d}'
    
    result = collection.insert_one(data)
    
    return jsonify({'message': 'Patient added', 'patientId': data['id'], '_id': str(result.inserted_id)}), 201

@app.route('/api/patients/<string:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """UPDATE: Modifies an existing patient record in MongoDB."""
    data = request.json
    role = data.pop('role', 'viewer')
    
    if not check_permission(role, 'update'):
        return jsonify({'message': 'Permission Denied: Cannot update records'}), 403

    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'message': 'Database connection failed'}), 500
        
    # MongoDB update query: Find by user-facing ID ('id'), set the new values
    result = collection.update_one(
        {'id': patient_id},
        {'$set': data}
    )
    
    if result.matched_count == 1:
        return jsonify({'message': f'Patient {patient_id} updated'}), 200
            
    return jsonify({'message': 'Patient not found'}), 404

@app.route('/api/patients/<string:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """DELETE: Removes a patient record from MongoDB."""
    data = request.json
    role = data.get('role', 'viewer')

    if not check_permission(role, 'delete'):
        return jsonify({'message': 'Permission Denied: Cannot delete records'}), 403

    collection = get_mongo_collection()
    if collection is None:
        return jsonify({'message': 'Database connection failed'}), 500

    result = collection.delete_one({'id': patient_id})
    
    if result.deleted_count == 1:
        return jsonify({'message': f'Patient {patient_id} deleted'}), 200
        
    return jsonify({'message': 'Patient not found'}), 404


if __name__ == '__main__':
    # Initialize connection to verify MongoDB is reachable
    _ = get_mongo_collection() 
    
    # Flask runs on http://127.0.0.1:5000/ by default
    app.run(debug=True)