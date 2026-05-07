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
