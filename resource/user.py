from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse

from model import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', required=True, type=str, help='username value must be set!')
_user_parser.add_argument('password', required=True, type=str, help='password value must be set!')


class User(Resource):
    def get(self, user_id):
        user = UserModel.get_user_by_id(id_=user_id)
        if not user:
            return {'message': 'no user found!'}, 404
        return user.json()

    def delete(self, user_id):
        user = UserModel.get_user_by_id(id_=user_id)
        if not user:
            return {'message': 'no user found!'}, 404
        user.delete_from_db()
        return {'message': 'user deleted!'}


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        username = data['username']
        password = data['password']
        if UserModel.get_user_by_username(username=username):
            return {'message': f'user {username} already exist!'}, 400
        user = UserModel(username=username, password=password)
        user.save_to_db()
        return {'message': f'user {username} added!'}, 201


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.get_user_by_username(data['username'])
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200
        return {'message': 'Invalid credentials'}, 401
