from workzeug.security import generate_password_hash, check_password_hash
from database_setup import db

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