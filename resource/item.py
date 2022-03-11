import sqlalchemy
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from model import ItemModel


class Item(Resource):
    @staticmethod
    def _req_parsing():
        parser = reqparse.RequestParser()
        parser.add_argument('price', required=True, type=float, help='price must be set!')
        parser.add_argument('store_id', required=True, type=int, help='store_id must be set!')
        data = parser.parse_args()
        return data

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'no such item!'}

    @jwt_required()
    def post(self, name):
        data = self._req_parsing()
        item = ItemModel(name=name, price=data['price'], store_id=data['store_id'])
        try:
            item.save_to_db()
            return item.json()
        except sqlalchemy.exc.IntegrityError:
            return {'message': f'item {name} already exists!'}, 400

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name=name)
        if item:
            item.delete_from_db()
            return {'message': f'item {name} deleted!'}, 200
        return {'message': 'no such item!'}

    @jwt_required()
    def put(self, name):
        data = self._req_parsing()
        item = ItemModel.find_by_name(name=name)
        if item:
            item.price = data['price']
            item.save_to_db()
            return item.json(), 201
        item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}