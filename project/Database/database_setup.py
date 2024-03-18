from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(100), nullable=False)

class UserChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    is_moderator = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('user_channels', lazy=True))
    channel = db.relationship('Channel', backref=db.backref('channel_users', lazy=True))
    db.UniqueConstraint('user_id', 'channel_id', name='unique_user_channel')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    channel = db.relationship('Channel', backref=db.backref('messages', lazy=True))
    sender = db.relationship('User', backref=db.backref('sent_messages', lazy=True))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Blocked'), nullable=False, default='Pending')
    user1 = db.relationship('User', foreign_keys=[user_id])
    user2 = db.relationship('User', foreign_keys=[friend_id])
    db.UniqueConstraint('user_id', 'friend_id', name='unique_friendship')

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blocked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blocker = db.relationship('User', foreign_keys=[user_id])
    blocked = db.relationship('User', foreign_keys=[blocked_user_id])
    db.UniqueConstraint('blocker_id', 'blocked_id', name='unique_block')
