import re

# -------------------------------
# 📧 EMAIL VALIDATION
# -------------------------------
def is_valid_email(email: str) -> bool:
    if not email:
        return False
    email = email.strip()
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None

# -------------------------------
# 📱 PHONE VALIDATION
# -------------------------------
def is_valid_phone(phone: str) -> bool:
    if not phone:
        return False
    phone = phone.strip()
    return re.fullmatch(r"\d{10}", phone) is not None

# -------------------------------
# 🔐 PASSWORD VALIDATION
# -------------------------------
def is_strong_password(password: str) -> bool:
    if not password:
        return False
    password = password.strip()
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# -------------------------------
# 👤 NAME VALIDATION
# -------------------------------
def is_valid_name(name: str) -> bool:
    if not name:
        return False
    name = name.strip()
    return re.fullmatch(r"[A-Za-z ]{3,}", name) is not None

# -------------------------------
# 🆔 STUDENT ID VALIDATION
# -------------------------------
def is_valid_student_id(student_id: str) -> bool:
    if not student_id:
        return False
    student_id = student_id.strip()
    return re.fullmatch(r"[A-Za-z0-9_-]{3,20}", student_id) is not None

# -------------------------------
# 🧑‍🏫 EMPLOYEE ID VALIDATION
# -------------------------------
def is_valid_employee_id(emp_id: str) -> bool:
    if not emp_id:
        return False
    emp_id = emp_id.strip()
    return re.fullmatch(r"[A-Za-z0-9_-]{3,20}", emp_id) is not None

# -------------------------------
# 📊 GENERIC REQUIRED CHECK
# -------------------------------
def is_not_empty(value: str) -> bool:
    return value is not None and str(value).strip() != ""

# -------------------------------
# 🔗 LINKEDIN VALIDATION
# -------------------------------
def is_valid_linkedin(url: str) -> bool:
    """Verifies if the string is a valid LinkedIn profile URL."""
    if not url:
        return False
    pattern = r"^https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$"
    return re.fullmatch(pattern, url.strip()) is not None

# -------------------------------
# 🛡️ SANITIZATION
# -------------------------------
def sanitize_text(text: str) -> str:
    """
    Cleans input strings by removing HTML and common injection traces.
    Useful for feedback and free-text fields displayed in the UI.
    """
    if not text:
        return ""
    # Remove HTML tags and replace dangerous characters
    clean = re.sub(r'<[^>]*>', '', str(text))
    clean = clean.replace("javascript:", "#").replace("<script", "#")
    return clean.strip()