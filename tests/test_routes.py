import pytest
from app import create_app, db
from app.models import Account

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_account(client):
    """Test creating a new account"""
    response = client.post('/accounts', json={
        "name": "John Doe",
        "email": "john@example.com",
        "address": "123 Main St"
    })
    assert response.status_code == 201
    assert response.get_json()['name'] == "John Doe"

def test_get_accounts(client):
    """Test retrieving account list"""
    response = client.get('/accounts')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_account(client):
    """Test retrieving a single account"""
    # First create one
    client.post('/accounts', json={"name": "Alice", "email": "alice@example.com"})
    response = client.get('/accounts/1')
    assert response.status_code == 200
    assert response.get_json()['name'] == "Alice"

def test_get_account_not_found(client):
    """Test retrieving an account that doesn't exist"""
    response = client.get('/accounts/999')
    assert response.status_code == 404

def test_update_account(client):
    """Test updating an account"""
    client.post('/accounts', json={"name": "Bob", "email": "bob@example.com"})
    response = client.put('/accounts/1', json={"name": "Robert"})
    assert response.status_code == 200
    assert response.get_json()['name'] == "Robert"

def test_delete_account(client):
    """Test deleting an account"""
    client.post('/accounts', json={"name": "Charlie", "email": "charlie@example.com"})
    response = client.delete('/accounts/1')
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get('/accounts/1')
    assert response.status_code == 404

def test_security_headers(client):
    """Test if security headers are present"""
    response = client.get('/accounts')
    assert 'X-Frame-Options' in response.headers
    assert 'X-Content-Type-Options' in response.headers
    assert 'Content-Security-Policy' in response.headers

def test_cors_headers(client):
    """Test if CORS headers are present"""
    response = client.get('/accounts')
    assert 'Access-Control-Allow-Origin' in response.headers
