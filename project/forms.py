from flask_wtf import FlaskForm
from sqlalchemy import String
from wtforms import (PasswordField, StringField, SubmitField,HiddenField, validators)
from wtforms.validators import InputRequired, Length, EqualTo, DataRequired, NumberRange

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
    channel_name = StringField('Channel Name', validators=[InputRequired(), Length(min=1, max=30)], render_kw={"placeholder": "Enter a channel name:"})
    chansubmit = SubmitField('Create Channel')

class MessageForm(FlaskForm):
    user_id = HiddenField('User ID', validators=[DataRequired(), NumberRange(min=1, message="Must be a positive Number")])
    channel_id = HiddenField('Channel ID', validators=[DataRequired(), NumberRange(min=1, message="Must be a positive Number")])
    message_text = StringField('Message Input', validators=[InputRequired()], render_kw={"placeholder": "Send a message"})
    message_submit = SubmitField('Send Message')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[InputRequired()], render_kw={"placeholder": "Current Password"})
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=8), EqualTo('confirm_new_password', message="Passwords must match.")], render_kw={"placeholder": "New Password"})
    confirm_new_password = PasswordField('Confirm New Password', validators=[InputRequired()], render_kw={"placeholder": "Confirm New Password"})
    submit = SubmitField('Change Password')

class EditUsernameForm(FlaskForm):
    new_username = StringField('New Username', validators=[InputRequired(), Length(min=1, max=50)])
    submit = SubmitField('Update Username')

class editDescriptionForm(FlaskForm):
    new_description = StringField('New Description', validators=[Length(min=0, max=500)])
    submit = SubmitField('Update Username')
