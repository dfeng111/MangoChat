from workzeug.security import generate_password_hash, check_password_hash
from database_setup import db, Message

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    received_messages = db.relationship('Message', backref='recipient', lazy=True)

    def set_password(self, passwd):
        self.password = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        return check_password_hash(self.password, passwd)

    def __repr__(self) -> str:
        return '<User: {}, Id: {}>'.format(self.username, self.id)
    
class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(100), nullable=False, unique=True)
    messages = db.relationship('Message', backref='channel', lazy=True)

    def register(self, user):
        self.users.append(user)
        message = Message(channel_id=self.id, sender_id=user.id, content=f"{user.username} has joined the channel.")
        db.session.add(message)
        db.session.commit()

    def unregister(self, user):
        self.users.remove(user)
        message = Message(channel_id=self.id, sender_id=user.id, content=f"{user.username} has left the channel.")
        db.session.add(message)
        db.session.commit()

    def notify_all(self, message):
        for user in self.users:
            new_message = Message(channel_id=self.id, sender_id=None, recipient_id=user.id, content=message)
            db.session.add(new_message)
        db.session.commit()