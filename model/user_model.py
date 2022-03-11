from loader import dbase


class UserModel(dbase.Model):
    __tablename__ = 'user'
    id = dbase.Column(dbase.Integer, primary_key=True)
    username = dbase.Column(dbase.String(80), unique = True)
    password = dbase.Column(dbase.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'user: "{self.username}", id: "{self.id}"'

    def json(self):
        return {'id': self.id, 'username': self.username}

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
