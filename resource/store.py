import sqlalchemy
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from model import StoreModel
from .decorators import admin_required, log_user

NAME_ALREADY_EXISTS = "A store with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."


class Store(Resource):
    @classmethod
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': STORE_NOT_FOUND}, 404

    @classmethod
    @jwt_required()
    @admin_required
    @log_user
    def post(cls, name):
        store = StoreModel(name)
        try:
            store.save_to_db()
            return store.json(), 201
        except sqlalchemy.exc.IntegrityError:
            return NAME_ALREADY_EXISTS.format(name), 400

    @classmethod
    @jwt_required()
    @admin_required
    @log_user
    def delete(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': STORE_DELETED}, 200


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {'stores': [store.json() for store in StoreModel.find_all()]}