from flask import session
from Database.database_setup import UserChannel

def get_current_user_id():
    """
    Get the ID of the currently logged-in user from the session.

    Returns:
        User ID if the user is logged in, otherwise None.
    """
    return session.get('user_id')

def is_user_channel_admin(user_id, channel_id, user_channel):
    """
    Check if the user with the given user_id is an admin of the channel with the given channel_id.

    Args:
        user_id: ID of the user
        channel_id: ID of the channel
        user_channel: UserChannel instance to check

    Returns:
        True if the user is an admin of the channel, False otherwise.
    """
    # Check if the user_channel exists and the user is a moderator
    if user_channel and user_channel.is_moderator:
        return True
    else:
        return False