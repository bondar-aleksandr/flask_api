from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from loader import db
from utils.db_api import DbIntegrityError


class Item(Resource):
    @staticmethod
    def _req_parsing():
        parser = reqparse.RequestParser()
        parser.add_argument('price', required=True, type=float, help='price must be set!')
        data = parser.parse_args()
        return data

    def get(self, name):
        item = db.get_item(name=name)
        if item:
            return item
        return {'message': 'no such item!'}

    @jwt_required()
    def post(self, name):
        data = self._req_parsing()
        try:
            db.add_item(name=name, price=data['price'])
            return db.get_item(name=name), 201
        except DbIntegrityError:
            return {'message': f'item {name} already exists!'}, 400

    @jwt_required()
    def delete(self, name):
        if db.get_item(name=name):
            db.delete_item(name=name)
            return {'message': f'item {name} deleted!'}, 200
        return {'message': 'no such item!'}

    @jwt_required()
    def put(self, name):
        data = self._req_parsing()
        db.modify_item(name=name, price=data['price'])
        return db.get_item(name=name), 201