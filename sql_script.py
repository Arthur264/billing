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
