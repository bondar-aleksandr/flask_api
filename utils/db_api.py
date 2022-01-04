import sqlite3

class DbIntegrityError(Exception):
    pass

class Database:
    def __init__(self, dbname):
        self.dbname = dbname

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
        self.connect_()
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

    def create_tables(self):
        sql = """
        CREATE TABLE if not exists "user" (
            "id"	INTEGER UNIQUE,
            "login"	TEXT UNIQUE,
            "password"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        self.execute(executescript=True, query=sql)

    def clear_db(self):
        sql = """
        delete from "user" where true
        """
        self.execute(executescript=True, query=sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' and '.join([
            f'{k}=?' for k in parameters.keys()
        ])
        params = tuple(parameters.values())
        return sql, params

    def add_user(self, login, password):
        query = 'insert into "user" (login, password) values (?,?)'
        try:
            self.execute(query=query, execute=True, data=(login, password))
        except sqlite3.IntegrityError:
            raise DbIntegrityError(f'user {login} already in DB!')

    def delete_user(self, **kwargs):
        base_sql = 'delete from "user" where '
        sql, params = self.format_args(base_sql, kwargs)
        try:
            self.execute(execute=True, query=sql, data=params)
        except sqlite3.OperationalError:
            print(f'No such column!')

    def get_user(self, **kwargs):
        base_sql = 'select * from "user" where '
        sql, params = self.format_args(base_sql, kwargs)
        result = None
        try:
            result = self.execute(fetchone=True, query=sql, data=params)
        except sqlite3.OperationalError:
            print(f'No such column!')
        return result

    def get_all_users(self):
        sql = 'select * from "user"'
        return self.execute(fetchall=True, query=sql)


if __name__ == '__main__':
    db = Database('user.db')
    db.create_tables()
    db.add_user(login='test01', password='pass01')
    db.add_user(login='test02', password='pass02')
    print(db.get_user(id='1', login='test01'))
    print(db.get_all_users())
