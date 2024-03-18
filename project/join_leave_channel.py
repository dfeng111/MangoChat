import pytest
from messaging import User, Channel

class User:
    def __init__(self, name):
        self.name = name
        self.received_messages = []

    def update(self, message):
        print(f"{self.name} received message: {message}")
        self.received_messages.append(message)

class Channel:
    def __init__(self):
        self.users = []  

    def register(self, user):
        self.users.append(user)
        self.notify_all(f"{user.name} has joined the channel.")

    def unregister(self, user):
        self.users.remove(user)
        self.notify_all(f"{user.name} has left the channel.")

    def notify_all(self, message):
        for user in self.users:
            user.update(message)

if __name__ == "__main__":
    # Channel is created
    channel = Channel()

    # Users are created
    user1 = User("Alice")
    user2 = User("Bob")

    # User1 joins the channel
    channel.register(user1)

    # User2 joins the channel
    channel.register(user2)

    # Message is sent to all users
    channel.notify_all("Hello everyone!")

    # User2 leaves the channel
    channel.unregister(user2)