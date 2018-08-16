SQL_ACCOUNT_TABLE = """ CREATE TABLE IF NOT EXISTS account_type (
                                id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                                name text UNIQUE NOT NULL
                            );"""
SQL_ACCOUNT_TYPE_TABLE = """ CREATE TABLE IF NOT EXISTS account (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                object_type text REFERENCES account_type(object_type) NOT NULL,
                                object_id text UNIQUE,
                                cost real
                            );"""

SQL_INSERT_ACCOUNT = """INSERT OR IGNORE INTO account(object_type, object_id, cost) VALUES (?, ?, ?);"""
SQL_INSERT_ACCOUNT_TYPE = """INSERT OR IGNORE INTO account_type(name) VALUES (?)"""
