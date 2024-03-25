# Run "python -im shell_setup" to test DB functionality and such

from flask import Flask
from app import app, db
from Database.database_setup import User, Channel, UserChannel, Message, Friend, Block
import sqlalchemy as sa
app.app_context().push()
