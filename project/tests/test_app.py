from flask_login import current_user
import pytest
from app import app
from Database.database_setup import db, User
from forms import RegisterForm, LoginForm

@pytest.fixture
def test_client():
    app.testing = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app.test_client()

def test_home_page(test_client):
    # Test home page
    response = test_client.get('/home', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to MangoChat' in response.data

def test_index_page(test_client):
    # Test index page
    response = test_client.get('/index', follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome to MangoChat' in response.data

@pytest.fixture
def make_test_user():
    test_user = User(username='john')
    test_user.set_password("Password123")
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
    loginform = LoginForm()
    loginform.username.data = 'john'
    loginform.password.data = 'Password123'
    response = test_client.post('/login', data=loginform.data, follow_redirects=True)
    assert response.status_code == 200
    # assert b'john' in response.data
    # assert b'Login Page' not in response.data  # Make sure login page content is not present

    # Test login with invalid credentials
    response = test_client.post('/login', data=dict(username='john', password='wrongpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
    assert b'Welcome back, john!' not in response.data  # Make sure success message is not present

def test_register_page(test_client):
    with app.app_context():
        response = test_client.get('/register', follow_redirects=True)
        assert response.status_code == 200
        assert b'Register' in response.data
        registerform = RegisterForm()
        registerform.username.data = 'jim'
        registerform.password.data = 'Password123'
        registerform.confirm_password.data = 'Password123'
        response = test_client.post('/register', data=registerform.data, follow_redirects=True)
        assert response.status_code == 200
        assert db.session.query(User).filter_by(username=registerform.username.data).first()
