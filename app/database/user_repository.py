from datetime import datetime


class UserRepository:

    def __init__(self, database):
        self.database = database

    def create_user(self, full_name, username, email, password, role="user"):
        return self.database.execute(
            """
            INSERT INTO users (full_name, username, email, password, role)
            VALUES (?, ?, ?, ?, ?)
            """,
            (full_name, username, email, password, role),
        )

    def get_by_email(self, email):
        return self.database.execute(
            """
            SELECT id, full_name, username, email, password, role, created_at, last_login
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    def get_by_username(self, username):
        return self.database.execute(
            """
            SELECT id, full_name, username, email, password, role, created_at, last_login
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    def get_by_id(self, user_id):
        return self.database.execute(
            """
            SELECT id, full_name, username, email, password, role, created_at, last_login
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    def get_all_users(self):
        return self.database.execute(
            """
            SELECT id, full_name, username, email, role, created_at, last_login
            FROM users
            ORDER BY full_name
            """
        ).fetchall()

    def username_exists(self, username):
        return self.database.execute(
            "SELECT 1 FROM users WHERE username = ? LIMIT 1",
            (username,),
        ).fetchone() is not None

    def email_exists(self, email):
        return self.database.execute(
            "SELECT 1 FROM users WHERE email = ? LIMIT 1",
            (email,),
        ).fetchone() is not None

    def update_last_login(self, user_id):
        timestamp = datetime.utcnow().isoformat(timespec="seconds")
        self.database.execute(
            "UPDATE users SET last_login = ? WHERE id = ?",
            (timestamp, user_id),
        )

    def update_password(self, email, password):
        self.database.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (password, email),
        )

    def get_user_choices(self):
        users = self.get_all_users()
        return [user["full_name"] or user["username"] or user["email"] for user in users]