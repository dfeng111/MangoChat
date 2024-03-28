from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    def set_password(self, passwd):
        self.password = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        return check_password_hash(self.password, passwd)

    def __repr__(self) -> str:
        return '<User: {}, Id: {}>'.format(self.username, self.id)

class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(100), nullable=False, unique=True)
    def __repr__(self) -> str:
        return '<Channel: {}, Id: {}>'.format(self.channel_name, self.id)

class UserChannel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    is_moderator = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('user_channels', lazy=True))
    channel = db.relationship('Channel', backref=db.backref('channel_users', lazy=True))
    db.UniqueConstraint('user_id', 'channel_id', name='unique_user_channel')
    def __repr__(self) -> str:
        return '<User: {}, Channel: {} Id: {}>'.format(self.user or self.user_id, self.channel or self.channel_id, self.id)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    channel = db.relationship('Channel', backref=db.backref('messages', lazy=True))
    sender = db.relationship('User', backref=db.backref('sent_messages', lazy=True))
    def __repr__(self) -> str:
        return '<Channel: {}, Sender: {}, Message: {}, id: {}>'.format(self.channel or self.channel_id, self.sender or self.sender.id, self.content, self.id)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Blocked'), nullable=False, default='Pending')
    user1 = db.relationship('User', foreign_keys=[user_id1])
    user2 = db.relationship('User', foreign_keys=[user_id2])
    db.UniqueConstraint('user_id1', 'user_id2', name='unique_friendship')
    def __repr__(self) -> str:
        return '<User1: {}, User2: {}, status: {}, id: {}>'.format(self.user1 or self.user_id1, self.user2 or self.user_id2, self.status, self.id)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blocker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blocked_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blocker = db.relationship('User', foreign_keys=[blocker_id])
    blocked = db.relationship('User', foreign_keys=[blocked_id])
    db.UniqueConstraint('blocker_id', 'blocked_id', name='unique_block')
    def __repr__(self) -> str:
        return '<Blocker: {}, Blocked: {}, id: {}>'.format(self.blocker or self.blocker_id, self.blocked or self.blocked_id, self.id)
