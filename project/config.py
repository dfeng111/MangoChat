import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'orange-ballroom-grape-boat-chair'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mango:COSC310=mcpw@127.0.0.1/mangochat'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
