from flask import Flask
from Database.database_setup import db, User, Friend, Block

class Block(db.Model):
    __tablename__ = 'block'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blocked_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Block {self.id}>"

def block_user(user_id, blocked_user_id):
    """
    Block a user by adding an entry to the Block table.
    
    Args:
        user_id: ID of the user performing the block.
        blocked_user_id: ID of the user to be blocked.
    
    Returns:
        Tuple (bool, str): Success status and message.
    """
    if user_id == blocked_user_id:
        return False, 'Cannot block yourself.'

    existing_block = Block.query.filter_by(user_id=user_id, blocked_user_id=blocked_user_id).first()

    if existing_block:
        return False, 'User already blocked.'

    block = Block(user_id=user_id, blocked_user_id=blocked_user_id)
    db.session.add(block)
    db.session.commit()
    return True, 'User blocked successfully.'

def unblock_user(user_id, blocked_user_id):
    """
    Unblock a user by removing the entry from the Block table.
    
    Args:
        user_id: ID of the user performing the unblock.
        blocked_user_id: ID of the user to be unblocked.
    
    Returns:
        Tuple (bool, str): Success status and message.
    """
    block = Block.query.filter_by(user_id=user_id, blocked_user_id=blocked_user_id).first()

    if not block:
        return False, 'User is not blocked.'

    db.session.delete(block)
    db.session.commit()
    return True, 'User unblocked successfully.'
