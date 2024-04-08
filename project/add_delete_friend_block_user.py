class User:
    def __init__(self, username):
        self.username = username
        self.friends = set()
        self.blocked = set()

class App:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return "User already exists."
        self.users[username] = User(username)
        return f"User {username} added."

    def add_friend(self, username, friend_username):
        if username not in self.users or friend_username not in self.users:
            return "One or both users not found."
        if friend_username in self.users[username].blocked or username in self.users[friend_username].blocked:
            return "Cannot add a blocked user as a friend."
        self.users[username].friends.add(friend_username)
        self.users[friend_username].friends.add(username)
        return f"Friend {friend_username} added to user {username}."

    def delete_friend(self, username, friend_username):
        if username not in self.users or friend_username not in self.users:
            return "One or both users not found."
        if friend_username not in self.users[username].friends:
            return "User is not a friend."
        self.users[username].friends.remove(friend_username)
        self.users[friend_username].friends.remove(username)
        return f"Friend {friend_username} removed from user {username}."

    def block_user(self, username, blocked_username):
        if username not in self.users or blocked_username not in self.users:
            return "One or both users not found."
        self.users[username].blocked.add(blocked_username)
        if blocked_username in self.users[username].friends:
            self.users[username].friends.remove(blocked_username)
        return f"User {blocked_username} blocked by user {username}."