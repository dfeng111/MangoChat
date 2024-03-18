import pytest
from delete_messages import UserWithDelete, ChannelWithDelete

def test_delete_message():
    # Channel is created      
    channel = ChannelWithDelete()

    # Userss are created
    user1 = UserWithDelete("Alice")
    user2 = UserWithDelete("Bob")

    # Users are registered to the channel
    channel.register(user1)
    channel.register(user2)

    # Message is sent to all users
    channel.notify_all("Hello everyone!")

    # Check to see if message was received 
    assert "Hello everyone!" in user1.received_messages
    assert "Hello everyone!" in user2.received_messages

    # Message is deleted for all users
    channel.delete_message("Hello everyone!")

    # Check that the message was deleted
    assert "Hello everyone!" not in user1.received_messages
    assert "Hello everyone!" not in user2.received_messages

    # User2 is unregistered
    channel.unregister(user2)

    # Check that user2 was unregistered
    assert user2 not in channel.users

    # Send another message
    channel.notify_all("User2 has left the channel.")

    # Check that the message was received by user1 but not user2
    assert "User2 has left the channel." in user1.received_messages
    assert "User2 has left the channel." not in user2.received_messages