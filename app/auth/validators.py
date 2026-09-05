def _clean_text(value):
    return (value or "").strip()


def _clean_email(value):
    return _clean_text(value).lower()


def _is_valid_email(email):
    if not email or "@" not in email:
        return False

    local_part, domain_part = email.split("@", 1)
    return bool(local_part.strip()) and bool(domain_part.strip()) and "." in domain_part


def validate_registration_data(full_name, username, email, password, confirm_password):
    full_name = _clean_text(full_name)
    username = _clean_text(username)
    email = _clean_email(email)

    if not full_name:
        return False, "Full Name is required."

    if not username:
        return False, "Username is required."

    if not email:
        return False, "Email is required."

    if not _is_valid_email(email):
        return False, "Please enter a valid email address."

    if not password:
        return False, "Password is required."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if password != confirm_password:
        return False, "Passwords do not match."

    return True, ""


def validate_login_data(email, password):
    email = _clean_email(email)

    if not email:
        return False, "Email is required."

    if not _is_valid_email(email):
        return False, "Please enter a valid email address."

    if not password:
        return False, "Password is required."

    return True, ""


def validate_reset_password_data(email, new_password, confirm_password):
    email = _clean_email(email)

    if not email:
        return False, "Email is required."

    if not _is_valid_email(email):
        return False, "Please enter a valid email address."

    if not new_password:
        return False, "New password is required."

    if len(new_password) < 6:
        return False, "Password must be at least 6 characters."

    if new_password != confirm_password:
        return False, "Passwords do not match."

    return True, ""