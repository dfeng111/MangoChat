import pytest
from flask import Flask
from Database.database_setup import db, User, Channel, UserChannel
from user_channel_relationship import join_channel, leave_channel

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

@pytest.fixture
def create_test_channel(app):
    with app.app_context():
        cname = "test_channel"
        test_channel = Channel(channel_name=cname)
        db.session.add(test_channel)
        db.session.commit()
        yield test_channel
        db.session.delete(test_channel)
        db.session.commit()

def test_join_channel(app, create_test_user, create_test_channel):
    test_user = create_test_user
    test_channel = create_test_channel
    
    # Test user joining the channel
    joined_user_channel = join_channel(test_user.id, test_channel.id)
    assert joined_user_channel is not None
    
    # Check if the user is in the channel
    with app.app_context():
        user_channels = UserChannel.query.filter_by(user_id=test_user.id, channel_id=test_channel.id).all()
        assert len(user_channels) == 1
        assert user_channels[0].user_id == test_user.id
        assert user_channels[0].channel_id == test_channel.id

def test_leave_channel(app, create_test_user, create_test_channel):
    test_user = create_test_user
    test_channel = create_test_channel
    
    # User joins the channel first
    joined_user_channel = join_channel(test_user.id, test_channel.id)
    assert joined_user_channel is not None
    
    # User leaves the channel
    left_channel = leave_channel(test_user.id, test_channel.id)
    assert left_channel is True
    
    # Check if the user is no longer in the channel
    with app.app_context():
        user_channels = UserChannel.query.filter_by(user_id=test_user.id, channel_id=test_channel.id).all()
        assert len(user_channels) == 0
