from Database.database_setup import db, User, Channel, Message

def send_message(channel_name, sender_name, message_content):
    # Find the channel by name and get its ID
    channel = Channel.query.filter_by(channel_name=channel_name).first()
    if not channel:
        return False, "Channel not found."

    # Find the user by name and get their ID
    sender = User.query.filter_by(username=sender_name).first()
    if not sender:
        return False, "User not found."

    # Create a new message with sender_id and channel_id
    new_message = Message(
        sender_id=sender.id,
        channel_id=channel.id,
        content=message_content
    )

    # Add the message to the database
    db.session.add(new_message)
    db.session.commit()

    return True, "Message sent successfully."