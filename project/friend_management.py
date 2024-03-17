from flask import Flask
from Database.database_setup import db, User, Friend, Block

app = Flask(__name__)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mango:COSC310=mcpw@127.0.0.1/mangochat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def add_friend(user_id, friend_id):
    if Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first():
        # Already friends
        return False, 'Already friends.'
    
    friendship = Friend(user_id=user_id, friend_id=friend_id)
    db.session.add(friendship)
    db.session.commit()
    return True, 'Friend added successfully.'

def remove_friend(user_id, friend_id):
    friendship = Friend.query.filter(
        (Friend.user_id == user_id and Friend.friend_id == friend_id) |
        (Friend.user_id == friend_id and Friend.friend_id == user_id)
    ).first()

    if not friendship:
        return False, 'Friendship not found.'

    db.session.delete(friendship)
    db.session.commit()
    return True, 'Friend removed successfully.'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()