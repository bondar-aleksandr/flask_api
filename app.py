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
        for item in items:
            if item['name'] == name:
                return item
        return {'status': 'no such item!'}, 404


    def post(self, name):
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