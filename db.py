import os
import sqlite3
from sqlite3 import Error


class Database(object):

    def __init__(self, db_name):
        db_path = os.path.join(os.getcwd(), db_name)
        self._connection = sqlite3.connect(db_path, timeout=10, check_same_thread=False)
        self.cur = self._connection.cursor()
        self.cur.execute("PRAGMA synchronous = OFF")
        self.cur.execute("PRAGMA journal_mode = MEMORY")

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
        try:
            self.cur.executemany(query, values)
        except (Error, sqlite3.Warning):
            for value in values:
                self.cur.execute(query, value)
        self.commit()
        return True

    def query(self, query):
        result = self.cur.execute(query).fetchall()
        return result

    def __del__(self):
        self._connection.close()
