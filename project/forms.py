from flask_wtf import FlaskForm
from sqlalchemy import String
from wtforms import (PasswordField, StringField, SubmitField, validators)
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "********"})
    logsubmit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], description="Enter your username", render_kw={"placeholder": "Create a username"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8), EqualTo('confirm_password', message="Passwords must match.")], render_kw={"placeholder": "Create a password"})
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired()], render_kw={"placeholder": "Confirm your password"})
    regsubmit = SubmitField('Register')

class ChannelForm(FlaskForm):
    channel_name = StringField('Channel Name', validators=[InputRequired(), Length(min=5)], render_kw={"placeholder": "Enter a channel name:"})
    chansubmit = SubmitField('Create Channel')

class MessageForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    message_text = StringField('Message Input', validators=[InputRequired()], render_kw={"placeholder": "Send a message"})
