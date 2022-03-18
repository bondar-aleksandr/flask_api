from loader import dbase
from datetime import datetime

class StoreModel(dbase.Model):
    __tablename__ = 'store'
    id = dbase.Column(dbase.Integer, primary_key=True)
    name = dbase.Column(dbase.String(80), unique=True)
    created = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    items = dbase.relationship('ItemModel', back_populates='store', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def __repr__(self):
        return f'store name: {self.name}'

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    def save_to_db(self):
        dbase.session.add(self)
        dbase.session.commit()

    def delete_from_db(self):
        dbase.session.delete(self)
        dbase.session.commit()