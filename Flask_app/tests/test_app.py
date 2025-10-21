import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_login(client):
    # Test registration page loads
    rv = client.get('/register')
    assert rv.status_code == 200

    # Test login page loads
    rv = client.get('/login')
    assert rv.status_code == 200
