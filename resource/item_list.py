from flask_restful import Resource
from model import ItemModel


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}