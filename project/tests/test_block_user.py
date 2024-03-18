import pytest
from flask import Flask
from Database.database_setup import db, User, Friend, Block
from project.block_user import block_user, unblock_user

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

def test_block_user(app):
    with app.app_context():
        # Create two users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Block user2 by user1
        result, message = block_user(user1.id, user2.id)
        assert result is True
        assert message == 'User blocked successfully.'

        # Check if user2 is in user1's blocked users
        block = Block.query.filter_by(user_id=user1.id, blocked_user_id=user2.id).first()
        assert block is not None

def test_unblock_user(app):
    with app.app_context():
        # Create two users
        user1 = User(username="user1", password="password1")
        user2 = User(username="user2", password="password2")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Block user2 by user1
        block_user(user1.id, user2.id)

        # Unblock user2 by user1
        result, message = unblock_user(user1.id, user2.id)
        assert result is True
        assert message == 'User unblocked successfully.'

        # Check if user2 is not in user1's blocked users
        block = Block.query.filter_by(user_id=user1.id, blocked_user_id=user2.id).first()
        assert block is None
