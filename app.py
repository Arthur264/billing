import io, os, csv, re
from sqlite3 import Error, IntegrityError
from db import Database
from sql_script import SQL_ACCOUNT_TABLE, SQL_ACCOUNT_TYPE_TABLE
FOLDER_NAME = 'tmp'

META_PATTERN = re.compile(r'v1:(.*):(.*):(.*):(.*)')
ROLES = ((1, 'env'), (2, 'farm'), (3, 'farm_role'), (4, 'server'))

class FieldsIndices(object):
    COST = 18
    SCALRMETA = 20

class Parser(object):
    SKIP_NAME = 'Cost'

    def __init__(self, file_name):
        self.db = Database('billing.db')
        self.file_name = file_name
        self.total_cost = {index:{} for index,_ in ROLES}
        self._create_account_table()

    def _skip_row(self, row):
        if not row or not row[FieldsIndices.SCALRMETA]:
            return True
        if not self._extract_meta(row[FieldsIndices.SCALRMETA]):
            return True
        if any([i for i in row if i == self.SKIP_NAME]):
            return True
        return False

    def _role_iter(self):
        for index, role in ROLES:
            yield (role, )

    def _create_account_table(self):
        self.db.query(SQL_ACCOUNT_TABLE)
        self.db.query(SQL_ACCOUNT_TYPE_TABLE)
        sql_insert_role = """INSERT OR IGNORE INTO account_type(name) VALUES (?)"""
        self.db.insert_many(sql_insert_role, self._role_iter())

    def _extract_meta(self, user_meta):
        return re.findall(META_PATTERN, user_meta)

    def _cost_iter(self):
        for role, values in self.total_cost.items():
            for _id, cost in values.items():
                yield (role, _id, cost)

    def _insert_cost(self):
        self.db.insert_many("INSERT OR IGNORE INTO account(object_type, object_id, cost) VALUES (?, ?, ?);", self._cost_iter())

    def process_row(self, row):
        meta_data = self._extract_meta(row[FieldsIndices.SCALRMETA])
        for index, _id in enumerate(meta_data[0], 1):
            if not _id:
                continue
            current_total = self.total_cost[index]
            current_total[_id] = current_total.get(_id, 0) + float(row[FieldsIndices.COST])

    def process_file(self, file_path):
        with io.open(file_path) as f:
            for row in csv.reader(f):
                if self._skip_row(row):
                    continue
                self.process_row(row)
        self._insert_cost()

    def start(self):
        file_path = os.path.join(FOLDER_NAME, self.file_name)
        self.process_file(file_path)
