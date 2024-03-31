from Database.database_setup import User, Channel

class UserWithDelete(User):
    def delete_message(self, message):
        if message in self.received_messages:
            self.received_messages.remove(message)

class ChannelWithDelete(Channel):
    def delete_message(self, message):
        for user in self.users:
            user.delete_message(message)

if __name__ == "__main__":
    # Channel is created      
    channel = ChannelWithDelete()

    # Users are created
    user1 = UserWithDelete("Alice")
    user2 = UserWithDelete("Bob")

    # Users are registered to the channel
    channel.register(user1)
    channel.register(user2)

    # Message is sent to all users
    channel.notify_all("Hello everyone!")

    # Message is deleted for all users
    channel.delete_message("Hello everyone!")

    # User2 is unregistered
    channel.unregister(user2)

    # Another message is sent
    channel.notify_all("User2 has left the channel.")