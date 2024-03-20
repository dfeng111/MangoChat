import pytest
from flask import Flask, session
from app import app
from utils import get_current_user_id, is_user_channel_admin
from Database.database_setup import UserChannel

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_current_user_id(client):
    # Test when user is not logged in
    with client:
        user_id = get_current_user_id()
        assert user_id is None

    # Test when user is logged in
    with client:
        with client.session_transaction() as sess:
            sess['user_id'] = 123
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
