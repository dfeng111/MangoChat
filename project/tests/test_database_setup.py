import pytest
from flask import Flask
from Database.database_setup import db, User, Channel, UserChannel, Message, Friend, Block

# Creating the Flask app and setting up the database
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mango:COSC310=mcpw@127.0.0.1/mangochat'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

# Creating a test user
def create_test_user(app):
    with app.app_context():
        test_user = User(username="test_user", password="test_password")
        db.session.add(test_user)
        db.session.commit()
        return test_user

# Creating a test channel
def create_test_channel(app):
    with app.app_context():
        test_channel = Channel(channel_name="test_channel")
        db.session.add(test_channel)
        db.session.commit()
        return test_channel

# Test cases for database models
def test_user_creation(app):
    test_user = create_test_user(app)
    assert test_user.id is not None

def test_channel_creation(app):
    test_channel = create_test_channel(app)
    assert test_channel.id is not None

def test_user_channel_relationship(app):
    test_user = create_test_user(app)
    test_channel = create_test_channel(app)

    with app.app_context():
        user_channel = UserChannel(user_id=test_user.id, channel_id=test_channel.id, is_moderator=True, is_banned=False)
        db.session.add(user_channel)
        db.session.commit()

        assert user_channel.id is not None

def test_message_creation(app):
    test_user = create_test_user(app)
    test_channel = create_test_channel(app)

    with app.app_context():
        message = Message(sender_id=test_user.id, channel_id=test_channel.id, content="Test Message")
        db.session.add(message)
        db.session.commit()

        assert message.id is not None

def test_friendship_creation(app):
    test_user1 = create_test_user(app)
    test_user2 = create_test_user(app)

    with app.app_context():
        friendship = Friend(user_id1=test_user1.id, user_id2=test_user2.id, status="Accepted")
        db.session.add(friendship)
        db.session.commit()

        assert friendship.id is not None

def test_block_creation(app):
    test_user1 = create_test_user(app)
    test_user2 = create_test_user(app)

    with app.app_context():
        block = Block(blocker_id=test_user1.id, blocked_id=test_user2.id)
        db.session.add(block)
        db.session.commit()

        assert block.id is not None

# Cleaning up test data after tests
def delete_test_data(app):
    with app.app_context():
        db.session.query(User).filter_by(username="test_user").delete()
        db.session.query(Channel).filter_by(channel_name="test_channel").delete()
        db.session.commit()

# Register the function to be run after each test
@pytest.fixture(autouse=True)
def run_after_test(app):
    yield
    delete_test_data(app)
