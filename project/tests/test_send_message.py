import pytest
from flask import Flask
from send_message import send_message
from Database.database_setup import db, User, Channel, Message

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

def test_send_message(app, create_test_user):
    # Create a test user
    test_user = create_test_user

    # Send a message to the test channel
    channel_name = 'Test Channel'
    message_content = 'Hello, this is a test message.'

    success, message = send_message(channel_name, test_user.username, message_content)

    # Check if the message was sent successfully
    assert success is True
    assert message == "Message sent successfully."

    # Query the message from the database to check if it was saved
    with app.app_context():
        saved_message = Message.query.filter_by(content=message_content).first()

        # Check if the saved message exists in the database
        assert saved_message is not None
        assert saved_message.content == message_content
        assert saved_message.sender.username == test_user.username
