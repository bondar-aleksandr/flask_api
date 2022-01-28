from flask_restful import Resource
from loader import db


class ItemList(Resource):
    def get(self):
        return {'items': db.get_all_items()}