import pytest
from flask import Flask
from Database.database_setup import db, User, Channel, UserChannel
from project.channel_management import create_channel, delete_channel, appoint_channel_admin

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
    db.session.delete(test_user)
    db.session.commit()

@pytest.fixture
def test_create_channel(app, create_test_user):
    # Create a test user
    test_user = create_test_user
    
    # Create a channel
    channel_name = "Test Channel"
    channel = create_channel(create_test_user.id, channel_name)

    # Check if channel is created
    assert channel is not None
    assert channel.channel_name == channel_name

    # Check if user is the admin of the channel
    user_channel = UserChannel.query.filter_by(user_id=create_test_user.id, channel_id=channel.id).first()
    assert user_channel is not None
    assert user_channel.is_moderator == True

def test_delete_channel(app, create_test_user):
    # Create a test user
    test_user = create_test_user

    # Create a channel
    channel_name = "Test Channel"
    channel = create_channel(test_user.id, channel_name)

    # Assign the user as admin of the test channel
    user_channel = UserChannel(user_id=test_user.id, channel_id=channel.id, is_moderator=True)
    db.session.add(user_channel)
    db.session.commit()

    # Delete the test channel
    result = delete_channel(channel.id)

    # Check if channel is deleted
    assert result == True
    assert db.session.get(Channel, channel.id) is None

    # Check if user-channel association is deleted
    assert db.session.query(UserChannel).filter_by(user_id=test_user.id, channel_id=channel.id).first() is None

def test_appoint_channel_admin(app, create_test_user):
    # Create a test user
    test_user = create_test_user

    # Create a channel
    channel_name = "Test Channel"
    channel = create_channel(test_user.id, channel_name)

    # Appoint the test user as admin
    result = appoint_channel_admin(test_user.id, channel.id)

    # Check if appointment was successful
    assert result is True

    # Check if the user is now an admin
    user_channel = UserChannel.query.filter_by(user_id=test_user.id, channel_id=channel.id).first()
    assert user_channel is not None
    assert user_channel.is_moderator is True