from flask_jwt_extended import get_jwt

def admin_required(func):
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims['is admin']:
            return func(*args, **kwargs)
        else:
            return {'message':'must be admin to make changes!'}, 401
    return wrapper