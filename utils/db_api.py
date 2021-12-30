import sqlite3
import uuid

class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.connection = None

    def connect_(self):
        try:
            self.connection = sqlite3.connect(self.dbname)
        except sqlite3.OperationalError:
            print(f'Cannot connect to {self.dbname}')

    def execute(self, query=None, data=None,
                fetchone: bool = False,
                fetchmany: bool = False,
                fetchall: bool = False,
                execute: bool = False,
                executemany: bool = False,
                executescript: bool = False
                ):
        with self.connection as con:
            self.connection: sqlite3.connect
            cur = self.connection.cursor()
            if execute:
                return con.execute(query, data)
            elif executemany:
                return con.executemany(query, data)
            elif executescript:
                return con.executescript(query)
            elif fetchone:
                if data:
                    cur.execute(query, data)
                else:
                    cur.execute(query)
                result = cur.fetchone()
                return result
            elif fetchmany:
                cur.execute(query, data)
                return cur.fetchmany(data)
            elif fetchall:
                if data:
                    cur.execute(query, data)
                else:
                    cur.execute(query)
                result = cur.fetchall()
                return result

    def create_db(self):
        command = open('create_db.sql').read()
        self.execute(executescript=True, query=command)

    # def clear_db(self):
    #     command =

    def add_user(self, login, password):
        query = 'insert into "user" (login, password) values (?,?)'
        try:
            self.execute(query=query, execute=True, data=(login, password))
        except sqlite3.IntegrityError:
            print(f'user {login} already in DB!')

    def get_user_by_login(self, login):
        query = 'select * from "user" where "login"=?'
        return self.execute(fetchone=True, query=query, data=(login,))
        # return self.execute(fetchone=True)

    def get_all_users(self):
        query = 'select * from "user"'
        return self.execute(fetchall=True, query=query)


if __name__ == '__main__':
    db = Database('testdb1')
    db.connect_()
    db.create_db()
    db.add_user(login='test03', password='pass03')
    print(db.get_user_by_login('test03'))
    print(db.get_all_users())
