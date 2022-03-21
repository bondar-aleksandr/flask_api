import sqlalchemy
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from model import ItemModel
from .decorators import admin_required, log_user

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."


class Item(Resource):
    @staticmethod
    def _req_parsing():
        parser = reqparse.RequestParser()
        parser.add_argument('price', required=True, type=float, help=BLANK_ERROR.format('price'))
        parser.add_argument('store_id', required=True, type=int, help=BLANK_ERROR.format('store_id'))
        data = parser.parse_args()
        return data

    @classmethod
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': ITEM_NOT_FOUND}

    @classmethod
    @jwt_required()
    @admin_required
    @log_user
    def post(cls, name):
        data = cls._req_parsing()
        item = ItemModel(name=name, price=data['price'], store_id=data['store_id'])
        try:
            item.save_to_db()
            return item.json()
        except sqlalchemy.exc.IntegrityError:
            return {'message': NAME_ALREADY_EXISTS.format(name)}, 400

    @classmethod
    @jwt_required()
    @admin_required
    @log_user
    def delete(cls, name):
        item = ItemModel.find_by_name(name=name)
        if item:
            item.delete_from_db()
            return {'message': ITEM_DELETED}, 200
        return {'message': ITEM_NOT_FOUND}, 400

    @classmethod
    @jwt_required()
    @admin_required
    @log_user
    def put(cls, name):
        data = cls._req_parsing()
        item = ItemModel.find_by_name(name=name)
        if item:
            item.price = data['price']
            item.save_to_db()
            return item.json(), 201
        item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': [item.json() for item in ItemModel.find_all()]}