import pytest
# from flask import Flask
from project.app import app
from Database.database_setup import db, User, Channel, UserChannel, Message, Friend, Block

# Creating the Flask app and setting up the database
@pytest.fixture
def test_app():
    # app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mango:COSC310=mcpw@127.0.0.1/mangochat'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.init_app(app)
    #
    # with app.app_context():
    #     db.create_all()
    with app.app_context():
        yield app

    # with app.app_context():
        # db.session.remove()
        # db.drop_all()

# Creating a test user
@pytest.fixture
def create_test_user():
    test_user = User(username="test_user", password="test_password")
    db.session.add(test_user)
    db.session.commit()
    yield test_user
    db.session.delete(test_user)

# Creating a test channel
@pytest.fixture
def create_test_channel():
    test_channel = Channel(channel_name="test_channel")
    db.session.add(test_channel)
    db.session.commit()
    yield test_channel
    db.session.delete(test_channel)

# Test cases for database models
def test_user_creation(test_app, create_test_user):
    assert create_test_user.id is not None

def test_channel_creation(test_app, create_test_channel):
    assert create_test_channel.id is not None

@pytest.fixture
def create_test_user_channel(test_app, create_test_user, create_test_channel):
    test_user = create_test_user
    test_channel = create_test_channel

    user_channel = UserChannel(user_id=test_user.id, channel_id=test_channel.id, is_moderator=True, is_banned=False)
    db.session.add(user_channel)
    db.session.commit()
    yield user_channel
    db.session.delete(user_channel)

def test_user_channel_relationship(test_app, create_test_user_channel):
    assert create_test_user_channel.id is not None

@pytest.fixture
def create_test_message(test_app, create_test_user, create_test_channel):
    test_user = create_test_user
    test_channel = create_test_channel

    message = Message(sender_id=test_user.id, channel_id=test_channel.id, content="Test Message")
    db.session.add(message)
    db.session.commit()
    yield message
    db.session.delete(message)
    
def test_message_creation(test_app, create_test_message):
    assert create_test_message.id is not None

@pytest.fixture
def create_friendship(test_app, create_test_user):
    test_user1 = create_test_user
    test_user2 = create_test_user

    friendship = Friend(user_id1=test_user1.id, user_id2=test_user2.id, status="Accepted")
    db.session.add(friendship)
    db.session.commit()
    yield friendship
    db.session.delete(friendship)


def test_friendship_creation(test_app, create_friendship):
    assert create_friendship.id is not None

@pytest.fixture
def create_block(test_app, create_test_user):
    test_user1 = create_test_user
    test_user2 = create_test_user

    block = Block(blocker_id=test_user1.id, blocked_id=test_user2.id)
    db.session.add(block)
    db.session.commit()
    yield block
    db.session.delete(block)

def test_block_creation(test_app, create_block):
    assert create_block.id is not None

# Cleaning up test data after tests
def delete_test_data(test_app):
    db.session.query(User).filter_by(username="test_user").delete()
    db.session.query(Channel).filter_by(channel_name="test_channel").delete()
    db.session.commit()

# Register the function to be run after each test
@pytest.fixture(autouse=True)
def run_after_test(test_app):
    yield
    delete_test_data(test_app)
