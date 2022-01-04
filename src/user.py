from loader import db

class User:
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    def __repr__(self):
        return f'user: "{self.username}", id: "{self.id}"'

    @classmethod
    def get_user_by_username(cls, username):
        result = db.get_user(login=username)
        if result:
            return cls(*result)

    @classmethod
    def get_user_by_id(cls, id_):
        result = db.get_user(id=id_)
        if result:
            return cls(*result)
