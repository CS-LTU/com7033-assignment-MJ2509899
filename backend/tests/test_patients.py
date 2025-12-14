"""Unit Tests for Patient Routes

Tests the patient management endpoints including:
- Fetching all patients
- Adding new patients
- Updating existing patients
- Deleting patients
- Error handling and validation
"""

import pytest
import json
from backend.app import app
from backend.db.db_sql import init_db, add_patient, delete_patient

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

@pytest.fixture
def sample_patient():
    """Sample patient data for testing"""
    return {
        'name': 'John Doe',
        'age': 45,
        'gender': 'Male',
        'hypertension': True,
        'heart_disease': False,
        'ever_married': 'Yes',
        'work_type': 'Private',
        'residence_type': 'Urban',
        'avg_glucose_level': 110.5,
        'bmi': 28.3,
        'smoking_status': 'never smoked',
        'stroke_prediction': 0.25
    }

@pytest.fixture
def authenticated_headers():
    """Mock JWT headers (authentication temporarily disabled)"""
    return {'Content-Type': 'application/json'}


class TestGetPatients:
    """Test suite for GET /api/patients/"""
    
    def test_get_all_patients_empty(self, client):
        """Test fetching patients when database is empty"""
        response = client.get('/api/patients/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_get_all_patients_with_data(self, client, sample_patient):
        """Test fetching patients with existing data"""
        # Add a patient first
        client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        # Fetch all patients
        response = client.get('/api/patients/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 1
        assert data[0]['name'] == sample_patient['name']


class TestAddPatient:
    """Test suite for POST /api/patients/"""
    
    def test_add_patient_success(self, client, sample_patient):
        """Test successfully adding a new patient"""
        response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == sample_patient['name']
        assert data['age'] == sample_patient['age']
        assert 'id' in data
    
    def test_add_patient_with_all_fields(self, client, sample_patient):
        """Test that all patient fields are saved correctly"""
        response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert data['hypertension'] == sample_patient['hypertension']
        assert data['heart_disease'] == sample_patient['heart_disease']
        assert data['avg_glucose_level'] == sample_patient['avg_glucose_level']
        assert data['bmi'] == sample_patient['bmi']
    
    def test_add_patient_missing_fields(self, client):
        """Test adding patient with missing required fields"""
        incomplete_patient = {
            'name': 'Jane Doe',
            'age': 50
            # Missing other required fields
        }
        
        response = client.post(
            '/api/patients/',
            data=json.dumps(incomplete_patient),
            content_type='application/json'
        )
        
        # Should fail due to missing fields
        assert response.status_code == 400


class TestUpdatePatient:
    """Test suite for PUT /api/patients/<id>"""
    
    def test_update_patient_success(self, client, sample_patient):
        """Test successfully updating a patient"""
        # Add patient first
        add_response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        patient_id = json.loads(add_response.data)['id']
        
        # Update patient data
        updated_data = sample_patient.copy()
        updated_data['name'] = 'Jane Updated'
        updated_data['age'] = 50
        
        response = client.put(
            f'/api/patients/{patient_id}',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Jane Updated'
        assert data['age'] == 50
    
    def test_update_nonexistent_patient(self, client, sample_patient):
        """Test updating a patient that doesn't exist"""
        response = client.put(
            '/api/patients/99999',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        assert response.status_code == 404


class TestDeletePatient:
    """Test suite for DELETE /api/patients/<id>"""
    
    def test_delete_patient_success(self, client, sample_patient):
        """Test successfully deleting a patient"""
        # Add patient first
        add_response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        patient_id = json.loads(add_response.data)['id']
        
        # Delete patient
        response = client.delete(f'/api/patients/{patient_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
    
    def test_delete_nonexistent_patient(self, client):
        """Test deleting a patient that doesn't exist"""
        response = client.delete('/api/patients/99999')
        
        assert response.status_code == 404
    
    def test_delete_patient_actually_removed(self, client, sample_patient):
        """Test that deleted patient is actually removed from database"""
        # Add patient
        add_response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        patient_id = json.loads(add_response.data)['id']
        
        # Delete patient
        client.delete(f'/api/patients/{patient_id}')
        
        # Try to fetch all patients - should not include deleted one
        get_response = client.get('/api/patients/')
        patients = json.loads(get_response.data)
        
        patient_ids = [p['id'] for p in patients]
        assert patient_id not in patient_ids


class TestPatientDataValidation:
    """Test suite for patient data validation"""
    
    def test_stroke_prediction_range(self, client, sample_patient):
        """Test that stroke prediction is within valid range (0-1)"""
        sample_patient['stroke_prediction'] = 0.75
        
        response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert 0 <= data['stroke_prediction'] <= 1
    
    def test_age_positive(self, client, sample_patient):
        """Test that age is positive"""
        response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert data['age'] > 0
    
    def test_bmi_positive(self, client, sample_patient):
        """Test that BMI is positive"""
        response = client.post(
            '/api/patients/',
            data=json.dumps(sample_patient),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        assert data['bmi'] > 0
