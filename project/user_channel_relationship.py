from Database.database_setup import db, User, Channel, UserChannel

def join_channel(user_id, channel_id, is_moderator=False):
    """
    Method to allow a user to join a channel.
    
    :param user_id: ID of the user who wants to join the channel
    :param channel_id: ID of the channel to join
    :param is_moderator: Boolean indicating if the user should be a moderator in the channel (default False)
    :return: UserChannel object representing the user's membership in the channel
    """
    user = User.query.get(user_id)
    channel = Channel.query.get(channel_id)
    
    if not user or not channel:
        raise ValueError("User or Channel not found")
    
    user_channel = UserChannel(user_id=user_id, channel_id=channel_id, is_moderator=is_moderator)
    
    db.session.add(user_channel)
    db.session.commit()
    
    return user_channel

def leave_channel(user_id, channel_id):
    """
    Method to allow a user to leave a channel.
    
    :param user_id: ID of the user who wants to leave the channel
    :param channel_id: ID of the channel to leave
    :return: True if user successfully left the channel, False otherwise
    """
    user_channel = UserChannel.query.filter_by(user_id=user_id, channel_id=channel_id).first()
    
    if not user_channel:
        raise ValueError("User is not in this channel")
    
    db.session.delete(user_channel)
    db.session.commit()
    
    return True