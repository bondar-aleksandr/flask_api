from flask_jwt import jwt_required
from flask_restful import Resource
from model import UserModel


class User(Resource):
    def get(self, user_id):
        user = UserModel.get_user_by_id(id_=user_id)
        if not user:
            return {'message': 'no user found!'}, 404
        return user.json()

    @jwt_required
    def delete(self, user_id):
        user = UserModel.get_user_by_id(id_=user_id)
        if not user:
            return {'message': 'no user found!'}, 404
        user.delete_from_db()
        return {'message': 'user deleted!'}