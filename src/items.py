from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from loader import db

#items = []
from utils.db_api import DbIntegrityError


class Item(Resource):
    @staticmethod
    def _req_parsing():
        parser = reqparse.RequestParser()
        parser.add_argument('price', required=True, type=float, help='price must be set!')
        data = parser.parse_args()
        return data

    def get(self, name):
        return db.get_item(name=name)

    #@jwt_required()
    def post(self, name):
        data = self._req_parsing()
        try:
            db.add_item(name=name, price=data['price'])
            return db.get_item(name=name), 201
        except DbIntegrityError:
            return {'message': f'item {name} already exists!'}, 400

    @jwt_required()
    def delete(self, name):
        global items
        if next(filter(lambda x: x['name'] == name, items), None):
            items = list(filter(lambda x: x['name'] != name, items))
            return {'message': 'item deleted!'}
        return {'message': 'no such item!'}

    @jwt_required()
    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            data = self._req_parsing()
            item.update({'name': name, 'price': data['price']})
            return item, 201
        else:
            return self.post(name)


class ItemList(Resource):
    def get(self):
        return {'items': items}