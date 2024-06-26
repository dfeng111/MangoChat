from Database.database_setup import Message, db, Channel, UserChannel

def create_channel(user_id, channel_name):
    """
    Create a new channel and assign the user as its admin.

    Args:
        user_id: ID of the user creating the channel.
        channel_name: Name of the new channel.

    Returns:
        The created Channel object.
    """
    # Create the channel
    channel = Channel(channel_name=channel_name)
    db.session.add(channel)
    db.session.commit()

    if channel is None:
        raise ValueError("Channel creation failed.")

    # Assign the user as admin of the channel
    user_channel = UserChannel(
        user_id=user_id,
        channel_id=channel.id,
        is_moderator=True  # Set as moderator/admin
    )
    db.session.add(user_channel)
    db.session.commit()

    return channel

def delete_channel(channel_id):
    """
    Delete a channel.

    Args:
        channel_id: ID of the channel to delete.

    Returns:
        True if deletion is successful, False otherwise.
    """
    # channel = Channel.query.get(channel_id)
    channel = db.session.query(Channel).get(channel_id)
    if channel:
        # Deletions are taken care of with on delete cascade.
        db.session.delete(channel)
        db.session.commit()
        return True
    return False

def appoint_channel_admin(user_id, channel_id):
    """
    Appoint a user as an admin of a channel.

    Args:
        user_id: ID of the user to appoint as admin.
        channel_id: ID of the channel.

    Returns:
        True if successful, False otherwise.
    """
    user_channel = UserChannel.query.filter_by(user_id=user_id, channel_id=channel_id).first()
    if user_channel:
        user_channel.is_moderator = True
        db.session.commit()
        return True
    return False
