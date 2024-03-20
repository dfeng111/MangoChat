import pytest
from flask import session
from app import app
from utils import get_current_user_id

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_client(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 123
    yield client

def test_get_current_user_id(client):
    with client:
        # Call the function to get user ID
        user_id = get_current_user_id()

        # Assert the user ID is None when not logged in
        assert user_id is None

def test_get_current_user_id_logged_in(logged_in_client):
    with logged_in_client:
        # Call the function to get user ID
        user_id = get_current_user_id()

        # Assert the user ID is as expected when logged in
        assert user_id == 123