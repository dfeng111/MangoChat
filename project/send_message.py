from Database.database_setup import db, User, Channel, Message

def send_message(channel_name, sender_username, message_content):
    # Get the channel and user objects
    channel = Channel.query.filter_by(channel_name=channel_name).first()
    sender = User.query.filter_by(username=sender_username).first()

    # Check if both channel and sender exist
    if channel is None:
        return False, "Channel does not exist." 
    
    if sender is None:
        return False, "Sender does not exist."

    # Create the message
    new_message = Message(channel, sender, message_content)

    try:
        # Add the message to the database
        db.session.add(new_message)
        db.session.commit()
        return True, "Message sent successfully."
    except Exception as e:
        # If there's an error, rollback the session and return an error message
        db.session.rollback()
        return False, "An error occurred while sending the message."
