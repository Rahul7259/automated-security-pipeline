# tests/test_app.py
import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_user_endpoint(client):
    response = client.get('/user?username=admin')
    assert response.status_code == 200

def test_ping_endpoint(client):
    response = client.get('/ping?host=127.0.0.1')
    assert response.status_code == 200

def test_greet_endpoint(client):
    response = client.get('/greet?name=Test')
    assert response.status_code == 200
    assert b'Hello, Test!' in response.data
