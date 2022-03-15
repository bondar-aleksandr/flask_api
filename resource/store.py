import sqlalchemy
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from model import StoreModel
from .decorators import admin_required


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'no such store'}, 404

    @jwt_required()
    @admin_required
    def post(self, name):
        store = StoreModel(name)
        try:
            store.save_to_db()
            return store.json(), 201
        except sqlalchemy.exc.IntegrityError:
            return {'message': f'item {name} already exists!'}, 400

    @jwt_required()
    @admin_required
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': f'store {name} deleted!'}, 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}