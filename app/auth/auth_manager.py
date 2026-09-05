from app.auth.password import hash_password, verify_password
from app.auth.validators import (
    validate_login_data,
    validate_registration_data,
    validate_reset_password_data,
)
from app.database.database import Database
from app.database.user_repository import UserRepository


class AuthManager:

    def __init__(self):

        self.db = Database()
        self.users = UserRepository(self.db)

    # ======================================================
    # Register New User
    # ======================================================

    def register(
        self,
        full_name,
        username,
        email,
        password,
        confirm_password
    ):

        is_valid, message = validate_registration_data(
            full_name,
            username,
            email,
            password,
            confirm_password,
        )

        if not is_valid:
            return False, message

        full_name = full_name.strip()
        username = username.strip()
        email = email.strip().lower()

        # -----------------------------
        # Check existing username/email
        # -----------------------------

        if self.users.username_exists(username) or self.users.email_exists(email):
            return False, "Username or Email already exists."

        # -----------------------------
        # Hash Password
        # -----------------------------

        hashed_password = hash_password(password)

        # -----------------------------
        # Insert User
        # -----------------------------

        self.users.create_user(
            full_name=full_name,
            username=username,
            email=email,
            password=hashed_password,
        )

        return True, "Account created successfully."

    # ======================================================
    # Login
    # ======================================================

    def login(
        self,
        email,
        password
    ):

        is_valid, message = validate_login_data(email, password)

        if not is_valid:
            return False, message

        email = email.strip().lower()

        user = self.users.get_by_email(email)

        if user is None:
            return False, "Invalid email or password."

        stored_password = user["password"] if isinstance(user, dict) or hasattr(user, "keys") else user[4]

        if not verify_password(password, stored_password):
            return False, "Invalid email or password."

        self.users.update_last_login(user["id"] if isinstance(user, dict) or hasattr(user, "keys") else user[0])

        return True, user

    # ======================================================
    # Reset Password
    # ======================================================

    def reset_password(self, email, new_password, confirm_password):

        is_valid, message = validate_reset_password_data(
            email,
            new_password,
            confirm_password,
        )

        if not is_valid:
            return False, message

        email = email.strip().lower()

        user = self.users.get_by_email(email)

        if user is None:
            return False, "No account found for that email."

        hashed_password = hash_password(new_password)

        self.users.update_password(email, hashed_password)

        return True, "Password updated successfully."

    # ======================================================
    # Get All Users
    # ======================================================

    def get_all_users(self):

        return self.users.get_all_users()

    def get_user_choices(self):

        users = self.get_all_users()
        choices = []

        for user in users:
            choices.append(user[1] or user[2] or user[3])

        return choices