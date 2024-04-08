from Database.database_setup import db, User, Channel, Message

def send_message(channel_id, sender_id, message_content):
    # Get the channel and user objects
    channel = Channel.query.get(channel_id)
    sender = User.query.get(sender_id)

    # Check if both channel and sender exist
    if not channel:
        return False, "Channel does not exist."
    
    if not sender:
        return False, "Sender does not exist."

    # Create the message
    new_message = Message(channel_id=channel_id, sender_id=sender_id, content=message_content)

    try:
        # Add the message to the database
        db.session.add(new_message)
        db.session.commit()
        return True, "Message sent successfully."
    except Exception as e:
        # If there's an error, rollback the session and return an error message
        db.session.rollback()
        return False, "An error occurred while sending the message."
