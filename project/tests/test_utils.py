from flask import session
from project.utils import get_current_user_id, is_user_channel_admin
from project.database_setup import UserChannel

# Mocking the session for testing purposes
class MockSession(dict):
    def __init__(self, *args, **kwargs):
        super(MockSession, self).__init__(*args, **kwargs)

def test_get_current_user_id():
    # Mock a logged-in user session
    with session_scope({'user_id': 123}):
        assert get_current_user_id() == 123

    # Test when user is not logged in
    with session_scope({}):
        assert get_current_user_id() is None

def test_is_user_channel_admin():
    # Mock UserChannel data - User is an admin
    user_channel_admin = MockUserChannel(user_id=1, channel_id=1, is_moderator=True)
    
    # Mock UserChannel data - User is not an admin
    user_channel_not_admin = MockUserChannel(user_id=2, channel_id=1, is_moderator=False)
    
    # Test case: User is an admin
    assert is_user_channel_admin(user_id=1, channel_id=1, mock_user_channel=user_channel_admin) is True

    # Test case: User is not an admin
    assert is_user_channel_admin(user_id=2, channel_id=1, mock_user_channel=user_channel_not_admin) is False

# Context manager for mocking session
def session_scope(session_data):
    original_session = session._get_current_object()
    session._get_current_object = lambda: MockSession(session_data)
    yield
    session._get_current_object = lambda: original_session

# Mocking the UserChannel model for testing purposes
class MockUserChannel:
    def __init__(self, user_id, channel_id, is_moderator):
        self.user_id = user_id
        self.channel_id = channel_id
        self.is_moderator = is_moderator