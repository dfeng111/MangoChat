import pytest
from flask import Flask
from Database.database_setup import db, User, Channel, Message
from message_management import send_message, delete_message

# Creating the Flask app and setting up the database
@pytest.fixture(autouse=True)
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

# Creating a test user
@pytest.fixture
def create_test_user(app):
    with app.app_context():
        uname = "test_user"
        test_user = User(username=uname, password="test_password")
        db.session.add(test_user)
        db.session.commit()
        yield test_user
        db.session.delete(test_user)
        db.session.commit()

# Creating a test channel
@pytest.fixture
def create_test_channel(app):
    with app.app_context():
        cname = "test_channel"
        test_channel = Channel(channel_name = cname)
        db.session.add(test_channel)
        db.session.commit()
        yield test_channel
        db.session.delete(test_channel)
        db.session.commit()

@pytest.fixture
def test_send_message(app, create_test_user, create_test_channel):
    # Create a test user and channel
    test_user = create_test_user
    test_channel = create_test_channel

    # Send a message to the test channel
    message_content = 'Hello, this is a test message.'
    success, message = send_message(test_channel.id, test_user.id, message_content)
    assert success is True
    assert message == "Message sent successfully."

    # Query the message from the database to check if it was saved
    with app.app_context():
        saved_message = Message.query.filter_by(content=message_content).first()

        # Check if the saved message exists in the database
        assert saved_message is not None
        assert saved_message.content == message_content
        assert saved_message.sender_id == test_user.id
        assert saved_message.channel_id == test_channel.id

# Testing delete_message function
def test_delete_message(app, create_test_user, create_test_channel, test_send_message):
    # Create a test user and channel
    test_user = create_test_user
    test_channel = create_test_channel

    # Send a message to the test channel
    message_content = 'This message will be deleted.'
    success, message = send_message(test_channel.id, test_user.id, message_content)
    assert success is True

    # Query the message from the database to check if it was saved
    with app.app_context():
        saved_message = Message.query.filter_by(content=message_content).first()
        assert saved_message is not None

        # Now let's try to delete the message
        success, message = delete_message(saved_message.id, test_user.id)
        assert success is True
        assert message == "Message deleted successfully."

        # Query the message again to check if it's deleted
        deleted_message = Message.query.get(saved_message.id)
        assert deleted_message is None