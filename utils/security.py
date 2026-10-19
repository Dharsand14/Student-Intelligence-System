import bcrypt
import jwt
import datetime
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


def _get_secret_key() -> str:
    try:
        secret = st.secrets["JWT_SECRET"]
    except (KeyError, StreamlitSecretNotFoundError) as exc:
        raise RuntimeError(
            "Set JWT_SECRET in Streamlit secrets before using password-reset tokens."
        ) from exc
    if not isinstance(secret, str) or not secret.strip():
        raise RuntimeError(
            "Set JWT_SECRET in Streamlit secrets before using password-reset tokens."
        )
    return secret


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False

# 🔐 JWT TOKENS
def create_reset_token(email: str, expires_in_minutes=30):
    """Generates a secure JWT token for password resets."""
    payload = {
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expires_in_minutes)
    }
    return jwt.encode(payload, _get_secret_key(), algorithm="HS256")

def verify_reset_token(token: str):
    """Decodes a JWT token and returns the email if valid."""
    try:
        payload = jwt.decode(token, _get_secret_key(), algorithms=["HS256"])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token