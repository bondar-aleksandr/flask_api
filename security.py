import logging

from model import UserModel


def authenticate(username, password):
    user = UserModel.get_user_by_username(username)
    if user and user.password == password:
        logging.info(f'user {user.username} logged in!')
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.get_user_by_id(user_id)