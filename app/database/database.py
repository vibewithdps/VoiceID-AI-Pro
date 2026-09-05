from pathlib import Path

import sqlite3

from app.database.migrations import migrate_database


class Database:

    def __init__(self, db_path="database/voiceid.db"):

        Path("database").mkdir(exist_ok=True)

        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        migrate_database(self.cursor)
        self.conn.commit()

    # -------------------------------------------------

    def create_tables(self):
        migrate_database(self.cursor)
        self.conn.commit()

    # -------------------------------------------------

    def execute(self, query, values=()):

        self.cursor.execute(query, values)

        self.conn.commit()

        return self.cursor

    # -------------------------------------------------

    def close(self):

        self.conn.close()