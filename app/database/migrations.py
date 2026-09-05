from app.database.models import Setting

DEFAULT_SETTINGS = (
    Setting("theme", "dark"),
    Setting("appearance", "dark"),
    Setting("default_sample_rate", "44100"),
    Setting("recording_duration", "5"),
    Setting("model_selection", "random_forest"),
)

def _table_columns(db, table_name):
    if db.is_postgres:
        db.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (table_name,))
        return {row[0] for row in db.cursor.fetchall()}
    else:
        db.cursor.execute(f"PRAGMA table_info({table_name})")
        return {row[1] for row in db.cursor.fetchall()}

def _add_column_if_missing(db, table_name, column_name, definition):
    if column_name not in _table_columns(db, table_name):
        db.cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")

def migrate_database(db):
    if db.is_postgres:
        pk_auto = "SERIAL PRIMARY KEY"
    else:
        pk_auto = "INTEGER PRIMARY KEY AUTOINCREMENT"

    db.execute(f"""
        CREATE TABLE IF NOT EXISTS users (
            id {pk_auto},
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    """)

    db.execute(f"""
        CREATE TABLE IF NOT EXISTS voice_samples (
            id {pk_auto},
            user_id INTEGER NOT NULL,
            audio_path TEXT NOT NULL,
            duration REAL,
            sample_number INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, sample_number)
        )
    """)

    db.execute(f"""
        CREATE TABLE IF NOT EXISTS trained_models (
            id {pk_auto},
            algorithm TEXT NOT NULL,
            accuracy REAL,
            model_path TEXT,
            trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.execute(f"""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id {pk_auto},
            user_id INTEGER,
            file_name TEXT NOT NULL,
            predicted_speaker TEXT NOT NULL,
            confidence REAL,
            prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    """)

    db.execute(f"""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    db.execute(f"""
        CREATE TABLE IF NOT EXISTS recordings (
            id {pk_auto},
            user_id INTEGER NOT NULL,
            speaker TEXT NOT NULL,
            file_path TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'recording',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    _add_column_if_missing(db, "users", "role", "TEXT NOT NULL DEFAULT 'user'")
    _add_column_if_missing(db, "users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    _add_column_if_missing(db, "users", "last_login", "TIMESTAMP")

    for setting in DEFAULT_SETTINGS:
        if db.is_postgres:
            db.execute(
                """
                INSERT INTO settings (key, value)
                VALUES (?, ?) ON CONFLICT (key) DO NOTHING
                """,
                (setting.key, setting.value),
            )
        else:
            db.execute(
                """
                INSERT OR IGNORE INTO settings (key, value)
                VALUES (?, ?)
                """,
                (setting.key, setting.value),
            )
