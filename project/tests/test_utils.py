import pytest
from flask import Flask, session
from app import app
from utils import get_current_user_id

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def logged_in_client(client):
    # Simulate a logged-in user by setting the session
    with client.session_transaction() as sess:
        sess['user_id'] = 123  # Simulate a user ID in the session
    yield client

def test_get_current_user_id(client):
    with client:
        # Call the function to get user ID
        user_id = get_current_user_id()

        # Assert the user ID is None since not logged in
        assert user_id is None

def test_get_current_user_id_logged_in(logged_in_client):
    with logged_in_client:
        # Call the function to get user ID
        user_id = get_current_user_id()

        # Assert the user ID is as expected (123)
        assert user_id == 123
