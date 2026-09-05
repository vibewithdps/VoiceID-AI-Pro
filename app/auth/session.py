class Session:
    """
    Stores the currently logged-in user.
    """

    _current_user = None
    _admin_usernames = {"dipendra", "sakshi"}

    @classmethod
    def login(cls, user):
        cls._current_user = user

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def current_user(cls):
        return cls._current_user

    @classmethod
    def get_user(cls):
        return cls._current_user

    @classmethod
    def is_logged_in(cls):
        return cls._current_user is not None

    @classmethod
    def user_id(cls):
        if cls._current_user:
            return cls._current_user[0]
        return None

    @classmethod
    def full_name(cls):
        if cls._current_user:
            return cls._current_user[1]
        return ""

    @classmethod
    def username(cls):
        if cls._current_user:
            return cls._current_user[2]
        return ""

    @classmethod
    def email(cls):
        if cls._current_user:
            return cls._current_user[3]
        return ""

    @classmethod
    def display_name(cls):
        if cls._current_user:
            return cls._current_user[1] or cls._current_user[2] or cls._current_user[3]
        return ""

    @classmethod
    def is_admin(cls):
        if not cls._current_user:
            return False

        username = (cls.username() or "").strip().lower()
        email = (cls.email() or "").strip().lower()

        return username in cls._admin_usernames or email.split("@")[0] in cls._admin_usernames