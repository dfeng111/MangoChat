from Database.database_setup import db, Channel, UserChannel

def create_channel(user_id, channel_name):
    """
    Create a new channel and assign the user as its admin.

    Requires:
        user_id: ID of the user creating the channel.
        channel_name: Name of the new channel.

    Modifies:
        Creates a new Channel object and a new UserChannel object.

    Effects:
        - Creates a new Channel with the provided name.
        - Creates a new UserChannel object linking the user to the channel as admin.

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

    Requires:
        channel_id: ID of the channel to delete.

    Modifies:
        Deletes the specified Channel and all associated UserChannel entries.

    Effects:
        - Deletes the specified Channel from the database.
        - Deletes all UserChannel entries associated with the specified channel.

    Returns:
        True if deletion is successful, False otherwise.
    """
    channel = db.session.query(Channel).get(channel_id)
    if channel:
        # Delete the channel and related user-channel associations
        UserChannel.query.filter_by(channel_id=channel_id).delete()
        db.session.delete(channel)
        db.session.commit()
        return True
    return False
