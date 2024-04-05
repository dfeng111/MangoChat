import pytest
from flask import session, Flask
from app import app
from send_message import send_message
from Database.database_setup import db, User, Channel, Message

@pytest.fixture
def app_with_session():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'  # Set a secret key for testing
    with app.test_request_context('/'):
        with app.test_client() as client:
            yield app
            session.clear()

@pytest.fixture(autouse=True)
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def setup_database(app):
    # Create test data for the database
    with app.app_context():
        # Create a test user
        user = User(username='test_user')
        db.session.add(user)
        db.session.commit()

        # Create a test channel
        channel = Channel(channel_name='test_channel')
        db.session.add(channel)
        db.session.commit()

        yield  # The test runs here

def test_send_message(app, app_with_session, setup_database):
    # Simulate a logged-in user by setting the session
    with app_with_session.test_request_context('/'):
        session['user_id'] = 1  # Assuming the test_user has ID 1

        # Send a message to the test channel
        channel_name = 'test_channel'
        sender_username = 'test_user'
        message_content = 'Hello, this is a test message.'

        success, message = send_message(channel_name, sender_username, message_content)

        # Assert that the message was sent successfully
        assert success is True
        assert message == "Message sent successfully."

        # Query the message from the database to check if it was saved
        saved_message = Message.query.filter_by(content=message_content).first()

        # Assert that the saved message exists in the database
        assert saved_message is not None
        assert saved_message.content == message_content
        assert saved_message.channel.channel_name == channel_name
        assert saved_message.sender.username == sender_username