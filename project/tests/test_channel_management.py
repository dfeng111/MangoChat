import pytest
from flask import Flask
from Database.database_setup import db, User, Channel, UserChannel, Message, Friend, Block
from project.channel_management import create_channel, delete_channel

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
def create_test_user():
    uname = "test_user"
    test_user = User(username=uname, password="test_password")
    db.session.add(test_user)
    db.session.commit()
    yield test_user
    # db.session.query(User).filter_by(username="test_user").delete()
    db.session.delete(test_user)
    db.session.commit()

# Creating a test channel
@pytest.fixture
def create_test_channel():
    test_channel = Channel(channel_name="test_channel")
    db.session.add(test_channel)
    db.session.commit()
    yield test_channel
    db.session.delete(test_channel)
    db.session.commit()

def test_create_channel(app, create_test_user):
    # Create a test user
    test_user = create_test_user

    # Create a channel
    channel_name = "Test Channel"
    channel = create_channel(test_user.id, channel_name)

    # Check if channel is created
    assert channel is not None
    assert channel.channel_name == channel_name

    # Check if user is the admin of the channel
    user_channel = UserChannel.query.filter_by(user_id=test_user.id, channel_id=channel.id).first()
    assert user_channel is not None
    assert user_channel.is_moderator == True

def test_delete_channel(app, create_test_user, create_test_channel):
    # Create a test user
    test_user = create_test_user

    # Create a test channel
    test_channel = create_test_channel

    # Assign the user as admin of the test channel
    user_channel = UserChannel(user_id=test_user.id, channel_id=test_channel.id, is_moderator=True)
    db.session.add(user_channel)
    db.session.commit()

    # Delete the test channel
    result = delete_channel(test_channel.id)

    # Check if channel is deleted
    assert result == True
    assert Channel.query.get(test_channel.id) is None

    # Check if user-channel association is deleted
    assert UserChannel.query.filter_by(user_id=test_user.id, channel_id=test_channel.id).first() is None