from flask_restful import Resource, reqparse
from model import UserModel


class UserRegister(Resource):
    @staticmethod
    def _req_parsing():
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, type=str, help='username value must be set!')
        parser.add_argument('password', required=True, type=str, help='password value must be set!')
        data = parser.parse_args()
        return data

    def post(self):
        data = self._req_parsing()
        username = data['username']
        password = data['password']
        if UserModel.get_user_by_username(username=username):
            return {'message': f'user {username} already exist!'}, 400
        user = UserModel(username=username, password=password)
        user.save_to_db()
        return {'message': f'user {username} added!'}, 201