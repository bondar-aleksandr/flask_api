from flask_jwt_extended import get_jwt, current_user
import logging


def admin_required(func):
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims['is admin']:
            return func(*args, **kwargs)
        else:
            return {'message':'must be admin to make changes!'}, 401
    return wrapper

def log_user(func):
    def wrapper(*args, **kwargs):
        user = current_user
        func_name = func.__name__
        logging.info(f'current user: {user.username}, method: {func_name}')
        return func(*args, **kwargs)
    return wrapper