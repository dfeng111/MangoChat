from Database.database_setup import db, Channel, UserChannel

def create_channel(user_id, channel_name):
    """
    Create a new channel and assign the user as its admin.

    Args:
        user_id: ID of the user creating the channel.
        channel_name: Name of the new channel.

    Returns:
        The created Channel object.
    """
    channel = Channel(channel_name=channel_name)
    db.session.add(channel)
    db.session.commit()

    # Assign the user as admin of the channel
    user_channel = UserChannel(
        user_id=user_id,
        channel_id=channel.id,
        is_moderator=True  # Set as moderator/admin
    )

    # Set user_channel user_id explicitly
    user_channel.user_id = user_id
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
    channel = Channel.query.get(channel_id)
    if channel:
        # Delete the channel and related user-channel associations
        UserChannel.query.filter_by(channel_id=channel_id).delete()
        db.session.delete(channel)
        db.session.commit()
        return True
    return False