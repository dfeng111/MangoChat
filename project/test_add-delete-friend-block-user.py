import pytest
from add_delete_friend_block_user import App

@pytest.fixture
def app_fixture(): 
    return App()

# adds a user to the app
def test_add_user(app_fixture):
    assert app_fixture.add_user('Alice') == 'User Alice added.'
    assert app_fixture.add_user('Alice') == 'User already exists.'

# adds a friend to the app
def test_add_friend(app_fixture):
    app_fixture.add_user('Alice')
    app_fixture.add_user('Bob')
    assert app_fixture.add_friend('Alice', 'Bob') == 'Friend Bob added to user Alice.'
    assert app_fixture.add_friend('Alice', 'Charlie') == 'One or both users not found.'

# deletes a friend from the app
def test_delete_friend(app_fixture):
    app_fixture.add_user('Alice')
    app_fixture.add_user('Bob')
    app_fixture.add_friend('Alice', 'Bob')
    assert app_fixture.delete_friend('Alice', 'Bob') == 'Friend Bob removed from user Alice.'
    assert app_fixture.delete_friend('Alice', 'Bob') == 'User is not a friend.'

# blocks a user from the app
def test_block_user(app_fixture):
    app_fixture.add_user('Alice')
    app_fixture.add_user('Bob')
    assert app_fixture.block_user('Alice', 'Bob') == 'User Bob blocked by user Alice.'
    assert app_fixture.block_user('Alice', 'Charlie') == 'One or both users not found.'