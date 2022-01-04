from loader import db
from flask_restful import Resource, reqparse
from utils.db_api import DbIntegrityError


class User:
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __repr__(self):
        return f'user: "{self.username}", id: "{self.id}"'

    @classmethod
    def get_user_by_username(cls, username):
        result = db.get_user(login=username)
        if result:
            return cls(*result)

    @classmethod
    def get_user_by_id(cls, id_):
        result = db.get_user(id=id_)
        if result:
            return cls(*result)

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
