from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
import logging

from resource import Item, ItemList, UserRegister, Store, StoreList, User, UserLogin
from loader import dbase

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    #level=logging.DEBUG,
                    )

app = Flask(__name__)
app.secret_key = 'key'
api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

app.config['TESTING'] = True
app.config['DEBUGING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'P@$$w0rd'

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    dbase.create_all()

if __name__ == '__main__':
    dbase.init_app(app)
    app.run()