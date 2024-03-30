import pytest
from project.messaging import User, Channel

@pytest.fixture
def user():
    return User("Alice")

@pytest.fixture
def channel():
    return Channel()

def test_user_initialization(user):
    assert user.name == "Alice"
    assert user.received_messages == []

def test_channel_initialization(channel):
    assert channel.users == []

def test_register_and_notify(channel, user):
    channel.register(user)

    message = f"{user.name} has joined the channel."
    channel.notify_all(message)

    assert user.received_messages == [message]

def test_unregister(channel, user):
    channel.register(user)

    message = f"{user.name} has left the channel."
    channel.unregister(user)

    assert user.received_messages == [message]