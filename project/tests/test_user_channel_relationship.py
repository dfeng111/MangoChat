import pytest
from user_channel_relationship import User, Channel, db, Message

@pytest.fixture
def user():
    user = User(username="test_user")
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()

@pytest.fixture
def channel():
    channel = Channel(channel_name="test_channel")
    db.session.add(channel)
    db.session.commit()
    yield channel
    db.session.delete(channel)
    db.session.commit()

def test_register(user, channel):
    assert len(channel.users) == 0
    channel.register(user)
    assert len(channel.users) == 1
    assert user in channel.users

def test_unregister(user, channel):
    channel.register(user)
    assert len(channel.users) == 1
    channel.unregister(user)
    assert len(channel.users) == 0
    assert user not in channel.users

def test_notify_all(user, channel):
    channel.register(user)
    assert len(channel.messages) == 0
    message = "Hello everyone!"
    channel.notify_all(message)
    assert len(channel.messages) == 1
    assert channel.messages[0].content == message
