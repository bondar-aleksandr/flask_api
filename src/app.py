from flask import Flask
from flask_restful import Api
from security import authenticate, identity
from flask_jwt import JWT
import logging
from user import UserRegister
from items import Item, ItemList

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

app.config['TESTING'] = True
app.config['DEBUGING'] = True

if __name__ == '__main__':
    app.run()