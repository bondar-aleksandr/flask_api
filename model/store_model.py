from typing import Dict, List, Union
from loader import dbase
from datetime import datetime
from model.item_model import ItemJSON


StoreJSON = Dict[str, Union[str, List[ItemJSON]]]


class StoreModel(dbase.Model):
    __tablename__ = 'store'
    id = dbase.Column(dbase.Integer, primary_key=True)
    name = dbase.Column(dbase.String(80), unique=True)
    created = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)
    items = dbase.relationship('ItemModel', back_populates='store', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_name(cls, name) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    def __repr__(self) -> str:
        return f'store name: {self.name}'

    def json(self) -> StoreJSON:
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    def save_to_db(self) -> None:
        dbase.session.add(self)
        dbase.session.commit()

    def delete_from_db(self) -> None:
        dbase.session.delete(self)
        dbase.session.commit()