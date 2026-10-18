from config.settings import ROLE_STUDENT, ROLE_STAFF

def get_role_from_email(email):
    """
    Automates the role assignment logic based on university email domains.
    Used during high-capacity student registration and staff onboarding.
    """
    if not email:
        return None
        
    email = email.lower().strip()

    if email.endswith("@staff.com"):
        return ROLE_STAFF

    elif email.endswith("@gmail.com"):
        return ROLE_STUDENT

    else:
        return "unknown"