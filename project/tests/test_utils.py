import pytest
from flask import session
from Database.database_setup import UserChannel
from project.utils import get_current_user_id, is_user_channel_admin
from project.app import app

class MockSession(dict):
    def __init__(self, *args, **kwargs):
        super(MockSession, self).__init__(*args, **kwargs)
        
class MockUserChannel:
    def __init__(self, user_id, channel_id, is_moderator):
        self.user_id = user_id
        self.channel_id = channel_id
        self.is_moderator = is_moderator

def test_get_current_user_id(app):
    # Simulate a logged-in user by setting the session
    with app.test_request_context('/'):
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 123

            # Call the function to get user ID
            user_id = get_current_user_id()

            # Assert the user ID is as expected
            assert user_id == 123

def test_is_user_channel_admin():
    # Mock UserChannel data - User is an admin
    user_channel_admin = MockUserChannel(user_id=1, channel_id=1, is_moderator=True)
    
    # Mock UserChannel data - User is not an admin
    user_channel_not_admin = MockUserChannel(user_id=2, channel_id=1, is_moderator=False)
    
    # Test case: User is an admin
    assert is_user_channel_admin(user_id=1, channel_id=1, user_channel=user_channel_admin) is True

    # Test case: User is not an admin
    assert is_user_channel_admin(user_id=2, channel_id=1, user_channel=user_channel_not_admin) is False

def session_scope(session_data):
    original_session = session._get_current_object()
    session._get_current_object = lambda: MockSession(session_data)
    yield
    session._get_current_object = lambda: original_session
