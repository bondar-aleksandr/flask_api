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
    req_data = request.get_json()
    new_store = {
        'name': req_data['name'],
        'items': []
    }
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
    req_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            item = {
                'name': req_data['name'],
                'price': req_data['price']
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