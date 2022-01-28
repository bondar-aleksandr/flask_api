import logging

from model import User


def authenticate(username, password):
    user = User.get_user_by_username(username)
    if user and user.password == password:
        logging.info(f'user {user.username} logged in!')
        return user


def identity(payload):
    user_id = payload['identity']
    return User.get_user_by_id(user_id)