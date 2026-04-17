import psycopg
from contextlib import contextmanager
from psycopg.rows import dict_row

class DatabaseManager:
    def __init__(self, dsn: str):
        self.dsn = dsn

    @contextmanager
    def connect(self, autocommit=False):
        with psycopg.connect(self.dsn, autocommit=autocommit, row_factory=dict_row) as conn:
            yield conn

    def query(self, sql: str, params=None, autocommit=True):
        with self.connect(autocommit=autocommit) as conn:
            return conn.execute(sql, params)