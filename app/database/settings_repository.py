class SettingsRepository:

    def __init__(self, database):
        self.database = database

    def get_all(self):
        rows = self.database.execute(
            "SELECT key, value FROM settings ORDER BY key"
        ).fetchall()
        return {row["key"]: row["value"] for row in rows}

    def get(self, key, default=None):
        row = self.database.execute(
            "SELECT value FROM settings WHERE key = ?",
            (key,),
        ).fetchone()
        return row["value"] if row else default

    def set(self, key, value):
        return self.database.execute(
            """
            INSERT INTO settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, str(value)),
        )

    def update_many(self, settings):
        for key, value in settings.items():
            self.set(key, value)