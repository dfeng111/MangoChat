from Database.database_setup import db, User, Channel, Message

# Function to send a message to a channel
def send_message(channel_name, sender_username, message_content):
    # Find the channel by name
    channel = Channel.query.filter_by(channel_name=channel_name).first()

    # Find the sender by username
    sender = User.query.filter_by(username=sender_username).first()

    if channel and sender:
        # Create a new message
        new_message = Message(
            channel_id=channel.id,
            sender_id=sender.id,
            content=message_content
        )

        # Add the message to the database session
        db.session.add(new_message)
        db.session.commit()

        return True, "Message sent successfully."
    else:
        return False, "Channel or sender not found."