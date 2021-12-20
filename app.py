import werkzeug.exceptions
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import logging
logging.basicConfig(level=logging.DEBUG)

items = [
]

app = Flask(__name__)
api = Api(app)

class Item(Resource):
    def get(self, name):
        item = filter(lambda x: x['name'] == name, items)
        return next(item, None), 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'item {name} already exists!'}, 400
        try:
            price = request.get_json()['price']
        except KeyError:
            return {'status': 'error - no price provided!'}, 400
        item = {'name': name, 'price': price}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)