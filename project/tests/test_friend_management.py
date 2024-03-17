import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Database.database_setup import db, User, Friend

# Import functions to test
from friend_management import add_friend, remove_friend

# Creating the Flask app and setting up the database
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Create some test users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_add_friend(app):
    # Get user IDs
    user1 = User.query.filter_by(username="user1").first()
    user2 = User.query.filter_by(username="user2").first()

    # Add a friend
    result = add_friend(user1.id, user2.id)
    assert result == "Friend added successfully."

    # Check if friendship exists
    friendship = Friend.query.filter_by(user_id=user1.id, friend_id=user2.id).first()
    assert friendship is not None

def test_add_friend_already_friends(app):
    # Get user IDs
    user1 = User.query.filter_by(username="user1").first()
    user2 = User.query.filter_by(username="user2").first()

    # Add a friend
    add_friend(user1.id, user2.id)

    # Add the same friend again (should fail)
    result = add_friend(user1.id, user2.id)
    assert result == "Already friends."

def test_remove_friend(app):
    # Get user IDs
    user1 = User.query.filter_by(username="user1").first()
    user2 = User.query.filter_by(username="user2").first()

    # Add a friend
    add_friend(user1.id, user2.id)

    # Remove the friend
    result = remove_friend(user1.id, user2.id)
    assert result == "Friend removed successfully."

    # Check if friendship is removed
    friendship = Friend.query.filter_by(user_id=user1.id, friend_id=user2.id).first()
    assert friendship is None

def test_remove_friend_not_found(app):
    # Get user IDs
    user1 = User.query.filter_by(username="user1").first()
    user2 = User.query.filter_by(username="user2").first()

    # Try to remove a friend that doesn't exist (should fail)
    result = remove_friend(user1.id, user2.id)
    assert result == "Friendship not found."