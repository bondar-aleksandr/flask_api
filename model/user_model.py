from datetime import datetime
from loader import dbase


class UserModel(dbase.Model):
    __tablename__ = 'user'
    id = dbase.Column(dbase.Integer, primary_key=True)
    username = dbase.Column(dbase.String(80), unique = True)
    password = dbase.Column(dbase.String(80))
    role = dbase.Column(dbase.String(80), nullable = False, default = 'ro')
    created = dbase.Column(dbase.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f'user: "{self.username}", id: "{self.id}"'

    def json(self):
        return {'id': self.id, 'username': self.username, 'role': self.role}

    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    def save_to_db(self):
        dbase.session.add(self)
        dbase.session.commit()

    def delete_from_db(self):
        dbase.session.delete(self)
        dbase.session.commit()
