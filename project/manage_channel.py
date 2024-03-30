from database_setup import db, Message

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