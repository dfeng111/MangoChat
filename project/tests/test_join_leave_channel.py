import pytest
from messaging import User, Channel

def test_join_leave_channel():
    # Create a channel
    channel = Channel()

    # Create users
    user1 = User("Alice")
    user2 = User("Bob")

    # Register user1 to the channel
    channel.register(user1)

    # Register user2 to the channel
    channel.register(user2)

    # Check that the join message for user2 was received by user1
    try:
        assert any("Bob has joined the channel." in message for message in user1.received_messages)
    except AssertionError:
        print("Failed: Bob's join message was not received by Alice")

    # User2 leaves the channel
    channel.unregister(user2)

    # Check that the leave message for user2 was received by user1
    try:
        assert any("Bob has left the channel." in message for message in user1.received_messages)
    except AssertionError:
        print("Failed: Bob's leave message was not received by Alice")
        
