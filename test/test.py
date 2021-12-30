from src.app import app
import json


def test_get_items_empty():
    with app.test_client() as client:
        response = client.get('/items')
        assert response.status_code == 200
        assert response.get_json() == {
            "items":[]
        }


def test_item_post():
    with app.test_client() as client:
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "price": 10.0
        }
        url = '/item/item01'

        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        assert response.get_json() == {
            "name":"item01",
            "price": 10.0
        }


def test_item_get():
    with app.test_client() as client:
        response = client.get('/item/item01')
        assert response.status_code == 200
        assert response.get_json() == {
            "name": "item01",
            "price": 10.0
        }


def test_item_get_non_existing():
    with app.test_client() as client:
        response = client.get('/item/item02')
        assert response.status_code == 200
        assert response.data == b'null\n'


def test_item_put():
    with app.test_client() as client:
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "price": 11.0
        }
        url = '/item/item01'

        response = client.put(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        assert response.get_json() == {
            "name": "item01",
            "price": 11.0
        }
        response = client.get('/item/item01')
        assert response.status_code == 200
        assert response.get_json() == {
            "name": "item01",
            "price": 11.0
        }


def test_item_put_non_existing():
    with app.test_client() as client:
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "price": 20.0
        }
        url = '/item/item02'

        response = client.put(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        assert response.get_json() == {
            "name": "item02",
            "price": 20.0
        }
        response = client.get('/item/item02')
        assert response.status_code == 200
        assert response.get_json() == {
            "name": "item02",
            "price": 20.0
        }


def test_item_del():
    with app.test_client() as client:
        response = client.delete('/item/item01')
        assert response.status_code == 200
        assert response.get_json() == {
            "message": "item deleted!"
        }


def test_item_del_non_existing():
    with app.test_client() as client:
        response = client.delete('/item/item01')
        assert response.status_code == 200
        assert response.get_json() == {
            "message": "no such item!"
        }

