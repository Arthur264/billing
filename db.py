import sqlite3
from sqlite3 import Error
import os


class Database(object):

    def __init__(self, db_name):
        db_path = os.path.join(os.getcwd(), db_name)
        self.connection = sqlite3.connect(db_path, timeout=1, check_same_thread=False, isolation_level=None)
        self.cur = self.connection.cursor()

    def remove_table(self, table_name):
        try:
            self.cur.execute("DROP TABLE {}".format(table_name))
        except Error as e:
            print (e)

    def insert(self, query):
        try:
            self.cur.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            self.connection.rollback()
            return False

    def insert_many(self, query, values):
        self.cur.executemany(query, values)
        self.connection.commit()
        result = self.cur.fetchall()
        return result


    def query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def __del__(self):
        self.connection.close()
