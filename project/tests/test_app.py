import pytest
from project.app import app
from Database.database_setup import db, User

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

@pytest.fixture
def make_test_user():
    test_user = User(username='john')
    test_user.set_password("password")
    with app.app_context():
        db.session.add(test_user)
        db.session.commit()
        yield test_user
        db.session.delete(test_user)
        db.session.commit()

def test_login_page(test_client, make_test_user):
    # Add a test user to the database
    user = make_test_user
    # Test login page GET request
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    # Test login with valid credentials
    response = test_client.post('/login', data=dict(logName='john', logPassword='password'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome back, john!' in response.data
    assert b'Login Page' not in response.data  # Make sure login page content is not present

    # Test login with invalid credentials
    response = test_client.post('/login', data=dict(logName='john', logPassword='wrongpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
    assert b'Welcome back, john!' not in response.data  # Make sure success message is not present


def test_success_page(test_client):
    # Test success page
    response = test_client.get('/success/john')
    assert response.status_code == 200
    assert b'Welcome back, john!' in response.data
