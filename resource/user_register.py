from loader import db
from flask_restful import Resource, reqparse
from utils.db_api import DbIntegrityError


class UserRegister(Resource):
    @staticmethod
    def _req_parsing():
        parser = reqparse.RequestParser()
        parser.add_argument('login', required=True, type=str, help='login value must be set!')
        parser.add_argument('password', required=True, type=str, help='password value must be set!')
        data = parser.parse_args()
        return data

    def post(self):
        data = self._req_parsing()
        login = data['login']
        password = data['password']
        try:
            db.add_user(login=login, password=password)
            return {'message':f'user {login} added!'}, 201
        except DbIntegrityError:
            return {'message':f'user {login} already exist!'}, 400
