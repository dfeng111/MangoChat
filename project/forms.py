from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, SubmitField)
from wtforms.validators import InputRequired, Length, EqualTo

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

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()], render_kw={"placeholder": "Current Password"})
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=8), EqualTo('confirm_new_password', message="Passwords must match.")], render_kw={"placeholder": "New Password"})
    confirm_new_password = PasswordField('Confirm New Password', validators=[InputRequired()], render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Change Password')