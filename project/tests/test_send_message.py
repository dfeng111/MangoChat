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

# Automatically called at the end of each test
@pytest.fixture(autouse=True)
def cleanup(app):
    with app.app_context():
        db.session.rollback()  # Rollback any uncommitted changes
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


def test_send_message(app, create_test_user, create_test_channel):
    # Create a test user and channel
    test_user = create_test_user
    test_channel = create_test_channel

    # Send a message to the test channel
    channel_name = test_channel.channel_name
    sender_name = test_user.username
    message_content = 'Hello, this is a test message.'
    success, message = send_message(channel_name, sender_name, message_content)
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