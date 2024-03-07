import pytest
from project.messaging.user import User
from project.messaging.channel import Channel

@pytest.fixture
def channel():
    return Channel()

@pytest.fixture
def users():
    user1 = User("Alice")
    user2 = User("Bob")
    return user1, user2

def test_register_and_notify(channel, users):
    user1, user2 = users
    channel.register(user1)
    channel.register(user2)

    message = "Hello everyone!"
    channel.notify_all(message)

    assert user1.received_messages == [message]
    assert user2.received_messages == [message]

def test_unregister(channel, users):
    user1, user2 = users
    channel.register(user1)
    channel.register(user2)

    message = "User2 has left the channel."
    channel.unregister(user2)

    channel.notify_all(message)

    assert user1.received_messages == [message]
    assert user2.received_messages == []

if __name__ == '__main__':
    pytest.main()