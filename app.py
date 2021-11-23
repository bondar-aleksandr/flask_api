import werkzeug.exceptions
from flask import Flask, jsonify, request

stores = [
    {
        'name': 'store_01',
        'items': [
            {
                'name': 'item01',
                'price': 10
            }
        ]
    }
]

app = Flask(__name__)

@app.route('/store', methods = ['POST'])
def create_store():
    try:
        req_data = request.get_json()
        new_store = {
            'name': req_data['name'],
            'items': []
        }
    except KeyError:
        return jsonify({'result': 'error: no name provided!'})
    except werkzeug.exceptions.BadRequest:
        return jsonify({'result': 'Wrong request format!'})


    stores.append(new_store)
    return jsonify({'result':'Success'})


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'result':f'error - No such store as {name}'})


@app.route('/store')
def get_stores():
    return jsonify({'stores':stores})


@app.route('/store/<string:name>/item', methods = ['POST'])
def create_item_in_store(name):
    try:
        item_name = request.get_json()['name']
        item_price = request.get_json()['price']
    except werkzeug.exceptions.BadRequest as e:
        return jsonify({'result': f'error: {e}'})
    except KeyError:
        return jsonify({'result': 'not enough info provided!'})
    for store in stores:
        if store['name'] == name:
            item = {
                'name': item_name,
                'price': item_price
            }
            store['items'].append(item)
            return jsonify(item)
    return jsonify({'result':'store not found'})


@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'result':f'error - No such store as {name}'})


if __name__ == '__main__':
    app.run(debug=True)