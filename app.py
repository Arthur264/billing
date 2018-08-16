import io
import os
import csv
import sys
import re
from db import Database
from sql_script import (
    SQL_ACCOUNT_TABLE,
    SQL_ACCOUNT_TYPE_TABLE,
    SQL_INSERT_ACCOUNT,
    SQL_INSERT_ACCOUNT_TYPE,
    SQL_UPDATE_ACCOUNT,
    SQL_EXIST_ACCOUNT
)

FOLDER_NAME = 'tmp'
DATABASE_NAME = 'billing.db'
META_PATTERN = re.compile(r'v1:(.*):(.*):(.*):(.*)')
ROLES = ((1, 'env'), (2, 'farm'), (3, 'farm_role'), (4, 'server'))


class FieldsIndices(object):
    COST = 18
    SCALRMETA = 20


class Parser(object):
    SKIP_NAME = 'Cost'

    def __init__(self, file_name):
        self._con = Database(DATABASE_NAME)
        self.file_name = file_name
        self.total_cost = {index: {} for index, _ in ROLES}

    def _skip_row(self, row):
        if not row or not row[FieldsIndices.SCALRMETA]:
            return True
        if not self._extract_meta(row[FieldsIndices.SCALRMETA]):
            return True
        if any([i for i in row if i == self.SKIP_NAME]):
            return True
        return False

    @staticmethod
    def _role_iter():
        for _, role in ROLES:
            yield (role,)

    def _create_account_table(self):
        account = self._con.query(SQL_EXIST_ACCOUNT)
        if account:
            return False
        self._con.query(SQL_ACCOUNT_TABLE)
        self._con.query(SQL_ACCOUNT_TYPE_TABLE)
        self._con.insert_many(SQL_INSERT_ACCOUNT_TYPE, self._role_iter())
        return True

    @staticmethod
    def _extract_meta(user_meta):
        return re.findall(META_PATTERN, user_meta)

    def _cost_iter(self, update=False):
        for role, values in self.total_cost.items():
            for _id, cost in values.items():
                if update:
                    yield (cost, _id, role)
                else:
                    yield (role, _id, cost)

    def _insert_cost(self):
        self._con.insert_many(SQL_UPDATE_ACCOUNT, self._cost_iter(update=True))
        self._con.insert_many(SQL_INSERT_ACCOUNT, self._cost_iter())
        return True

    def process_row(self, row):
        meta_data = self._extract_meta(row[FieldsIndices.SCALRMETA])
        for index, _id in enumerate(meta_data[0], 1):
            if not _id:
                continue
            current_total = self.total_cost[index]
            current_total[_id] = current_total.get(_id, 0) + float(row[FieldsIndices.COST])

    def process_file(self, file_path):
        with io.open(file_path) as infile:
            for row in csv.reader(infile):
                if self._skip_row(row):
                    continue
                self.process_row(row)
        return self._insert_cost()

    def start(self):
        self._create_account_table()
        file_path = os.path.join(FOLDER_NAME, self.file_name)
        self.process_file(file_path)
