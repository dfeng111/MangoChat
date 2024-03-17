from flask import Flask
from Database.database_setup import db, User, Friend, Block

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mango:COSC310=mcpw@127.0.0.1/mangochat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def add_friend(user_id, friend_id):
    """
    Add a friend to the user's friend list.
    """
    user = User.query.get(user_id)
    friend = User.query.get(friend_id)

    if not user or not friend:
        return "User or friend not found."

    # Check if they are already friends
    if Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first():
        return "Already friends."

    new_friendship = Friend(user_id=user_id, friend_id=friend_id)
    db.session.add(new_friendship)
    db.session.commit()
    return "Friend added successfully."

def remove_friend(user_id, friend_id):
    """
    Remove a friend from the user's friend list.
    """
    friendship = Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first()

    if not friendship:
        return "Friendship not found."

    db.session.delete(friendship)
    db.session.commit()
    return "Friend removed successfully."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()