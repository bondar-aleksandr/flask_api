from flask_jwt_extended import current_user

from loader import dbase
from datetime import datetime


class ItemModel(dbase.Model):
    __tablename__ = 'item'
    id = dbase.Column(dbase.Integer, primary_key = True)
    name = dbase.Column(dbase.String(80), unique = True)
    price = dbase.Column(dbase.Float)
    created = dbase.Column(dbase.DateTime, nullable = False, default = datetime.utcnow)
    modified = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    store_id = dbase.Column(dbase.Integer, dbase.ForeignKey('store.id'))
    modified_by = dbase.Column(dbase.Integer, dbase.ForeignKey('user.id'))
    store = dbase.relationship('StoreModel', back_populates='items')

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def __repr__(self):
        return f'item name: {self.name}, item price: {self.price}'

    def json(self):
        return {"name": self.name, "price": self.price, "store": self.store.name}

    def save_to_db(self):
        self.modified_by = current_user.id
        self.modified = datetime.utcnow()
        dbase.session.add(self)
        dbase.session.commit()

    def delete_from_db(self):
        dbase.session.delete(self)
        dbase.session.commit()
