from flask import Flask
from flask_restful import Api

from security import authenticate, identity
from flask_jwt import JWT
import logging
from resource import Item, ItemList, UserRegister, Store, StoreList
from loader import dbase

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    #level=logging.DEBUG,
                    )

app = Flask(__name__)
app.secret_key = 'key'
api = Api(app)

jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

app.config['TESTING'] = True
app.config['DEBUGING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_first_request
def create_tables():
    dbase.init_app(app)
    dbase.create_all()


if __name__ == '__main__':
    app.run()