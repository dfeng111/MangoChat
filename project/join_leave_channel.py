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
        message = f"{user.name} has joined the channel."
        self.notify_all(message)
        self.users.append(user)

    def unregister(self, user):
        self.users.remove(user)
        self.notify_all(f"{user.name} has left the channel.")

    def notify_all(self, message):
        for user in self.users:
            user.update(message)

if __name__ == "__main__":
    # Create a channel
    channel = Channel()

    # Create users
    user1 = User("Alice")  
    user2 = User("Bob")

    # Register users to the channel
    channel.register(user1)  
    channel.register(user2)

    # Send a message to all users
    channel.notify_all("Hello everyone!")
    
    # Unregister user2
    channel.unregister(user2)

    # Send another message
    channel.notify_all("User2 has left the channel.")
    
    