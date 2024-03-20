import pytest
from flask import session
from app import app
from utils import get_current_user_id, is_user_channel_admin
from Database.database_setup import UserChannel

@pytest.fixture
def app_with_session():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'  # Set a secret key for testing
    with app.test_request_context('/'):
        with app.test_client() as client:
            yield app
            session.clear()

def test_get_current_user_id_logged_in(app_with_session):
    # Simulate a logged-in user by setting the session
    with app_with_session.test_request_context('/'):
        session['user_id'] = 123
        user_id = get_current_user_id()
        assert user_id == 123

def test_is_user_channel_admin():
    # Mock UserChannel data - User is an admin
    user_channel_admin = UserChannel(user_id=1, channel_id=1, is_moderator=True)
    
    # Mock UserChannel data - User is not an admin
    user_channel_not_admin = UserChannel(user_id=2, channel_id=1, is_moderator=False)
    
    # Test case: User is an admin
    assert is_user_channel_admin(user_id=1, channel_id=1, user_channel=user_channel_admin) is True

    # Test case: User is not an admin
    assert is_user_channel_admin(user_id=2, channel_id=1, user_channel=user_channel_not_admin) is False
