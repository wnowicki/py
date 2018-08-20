import mysql.connector
import configuration


def connect():
    conf = configuration.load('config.json')

    return mysql.connector.connect(
        host=conf['mysql']['host'],
        user=conf['mysql']['user'],
        passwd=conf['mysql']['passwd'],
        port=conf['mysql']['port'],
        database=conf['mysql']['database']
    )


class Database:
    def __init__(self, host=None, user=None, password=None, port=None, databaes=None):
        self._db = connect()

    def get_cursor(self):
        return self._db.cursor()

    def fetch_dict(self, query):
        cursor = self.get_cursor()
        cursor.execute(query)
        names = [d[0] for d in cursor.description]
        return [dict(zip(names, row)) for row in cursor.fetchall()]

    def execute(self, query):
        cursor = self.get_cursor()
        cursor.execute(query)
        return cursor.fetchall()
