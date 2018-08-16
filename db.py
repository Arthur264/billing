import os
import sqlite3
from sqlite3 import Error


class Database(object):

    def __init__(self, db_name):
        db_path = os.path.join(os.getcwd(), db_name)
        self._connection = sqlite3.connect(db_path, timeout=20, check_same_thread=False, isolation_level=None)
        self.cur = self._connection.cursor()
        self.cur.execute("PRAGMA journal_mode=WAL")

    def remove_table(self, table_name):
        try:
            self.cur.execute("DROP TABLE {}".format(table_name))
            return True
        except Error:
            return None

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def insert(self, query):
        try:
            self.cur.execute(query)
            self.commit()
            return True
        except Error:
            self.rollback()
            return False

    def insert_many(self, query, values):
        result = self.cur.executemany(query, values).fetchall()
        self.commit()
        return result

    def query(self, query):
        result = self.cur.execute(query).fetchall()
        return result

    def __del__(self):
        self._connection.close()
