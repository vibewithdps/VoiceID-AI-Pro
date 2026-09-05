from app.database.models import Setting


DEFAULT_SETTINGS = (
    Setting("theme", "dark"),
    Setting("appearance", "dark"),
    Setting("default_sample_rate", "44100"),
    Setting("recording_duration", "5"),
    Setting("model_selection", "random_forest"),
)


def _table_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def _add_column_if_missing(cursor, table_name, column_name, definition):
    if column_name not in _table_columns(cursor, table_name):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def migrate_database(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS voice_samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            audio_path TEXT NOT NULL,
            duration REAL,
            sample_number INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, sample_number)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trained_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            algorithm TEXT NOT NULL,
            accuracy REAL,
            model_path TEXT,
            trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT NOT NULL,
            predicted_speaker TEXT NOT NULL,
            confidence REAL,
            prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            speaker TEXT NOT NULL,
            file_path TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'recording',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    _add_column_if_missing(cursor, "users", "role", "TEXT NOT NULL DEFAULT 'user'")
    _add_column_if_missing(cursor, "users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    _add_column_if_missing(cursor, "users", "last_login", "TIMESTAMP")

    for setting in DEFAULT_SETTINGS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO settings (key, value)
            VALUES (?, ?)
            """,
            (setting.key, setting.value),
        )