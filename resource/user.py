from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_restful import Resource, reqparse
from model import UserModel
from .decorators import admin_required
import logging

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', required=True, type=str, help='username value must be set!')
_user_parser.add_argument('password', required=True, type=str, help='password value must be set!')
_user_parser.add_argument('role', required = False, type=str, help='user role should be set!')


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.get_user_by_id(id_=user_id)
        if not user:
            return {'message': 'no user found!'}, 404
        return user.json()

    @classmethod
    @jwt_required()
    @admin_required
    def delete(cls, user_id):
        user = UserModel.get_user_by_id(id_=user_id)
        if not user:
            return {'message': 'no user found!'}, 404
        user.delete_from_db()
        return {'message': 'user deleted!'}


class UserRegister(Resource):
    @classmethod
    @jwt_required()
    @admin_required
    def post(cls):
        data = _user_parser.parse_args()
        username = data['username']
        password = data['password']
        role = data['role']
        if UserModel.get_user_by_username(username=username):
            return {'message': f'user {username} already exist!'}, 400
        user = UserModel(username=username, password=password, role=role)
        user.save_to_db()
        return {'message': f'user {username} added!'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.get_user_by_username(data['username'])
        if user and user.password == data['password']:
            if user.role == 'rw':
                additional_claims = {'is admin': True}
            else:
                additional_claims = {'is admin': False}
            access_token = create_access_token(identity=user.id, fresh=True, additional_claims=additional_claims)
            refresh_token = create_refresh_token(user.id)
            logging.info(f'user: {user.username} logged in!')
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, 200
        return {'message': 'Invalid credentials'}, 401
