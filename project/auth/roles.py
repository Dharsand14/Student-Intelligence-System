def get_role_from_email(email):
    email = email.lower()

    if email == "admin@gmail.com":
        return "admin"

    elif email.endswith("@staff.com"):
        return "staff"

    elif email.endswith("@gmail.com"):
        return "student"

    else:
        return "unknown"