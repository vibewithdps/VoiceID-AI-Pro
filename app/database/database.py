import os
from pathlib import Path

class Database:
    def __init__(self, db_path="database/voiceid.db"):
        self.db_url = os.environ.get("DATABASE_URL")
        
        if self.db_url:
            self.is_postgres = True
            import psycopg2
            from psycopg2.extras import DictCursor
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        else:
            self.is_postgres = False
            import sqlite3
            Path("database").mkdir(exist_ok=True)
            self.db_path = Path(db_path)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

        from app.database.migrations import migrate_database
        migrate_database(self)

    def create_tables(self):
        from app.database.migrations import migrate_database
        migrate_database(self)

    def execute(self, query, values=()):
        if self.is_postgres:
            # Simple replacement for parameterized queries
            query = query.replace("?", "%s")
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor

    def close(self):
        self.conn.close()
