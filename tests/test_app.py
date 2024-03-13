import pytest
from project.app import app

@pytest.fixture
def test_client():
    app.testing = True
    return app.test_client()

def test_home_page(test_client):
    # Test home page
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Hello World!"

def test_index_page(test_client):
    # Test index page
    response = test_client.get('/index')
    assert response.status_code == 200
    assert b'Yo Country' in response.data

def test_login_page(test_client):
    # Test login page GET request
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

    # Test login with valid credentials
    response = test_client.post('/login', data=dict(logName='john', logPassword='password'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back, john!' in response.data

    # Test login with invalid credentials
    response = test_client.post('/login', data=dict(logName='john', logPassword='wrongpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_success_page(test_client):
    # Test success page
    response = test_client.get('/success/john')
    assert response.status_code == 200
    assert b'Welcome back, john!' in response.data
