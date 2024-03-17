import pytest
from flask import Flask
from Database.database_setup import db, User, Channel, UserChannel, Message, Friend, Block
from friend_management import add_friend, remove_friend

# Creating the Flask app and setting up the database
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

def test_add_friend(app):
    with app.app_context():
        # Creating two users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Adding user2 as a friend of user1
        result, message = add_friend(user1.id, user2.id)
        assert result is True
        assert message == 'Friend added successfully.'

def test_add_friend_already_friends(app):
    with app.app_context():
        # Creating two users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Adding user2 as a friend of user1
        add_friend(user1.id, user2.id)

        # Attempting to add user2 again, they should already be friends
        result, message = add_friend(user1.id, user2.id)
        assert result is False
        assert message == 'Already friends.'

def test_remove_friend(app):
    with app.app_context():
        # Creating two users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Adding user2 as a friend of user1
        add_friend(user1.id, user2.id)

        # Removing user2 as a friend of user1
        result, message = remove_friend(user1.id, user2.id)
        assert result is True
        assert message == 'Friend removed successfully.'

def test_remove_friend_not_found(app):
    with app.app_context():
        # Creating two users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Removing user2 as a friend of user1 without adding first
        result, message = remove_friend(user1.id, user2.id)
        assert result is False
        assert message == 'Friendship not found.'