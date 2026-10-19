import pytest
import jwt
import datetime
import time
import os
import sys
from types import SimpleNamespace

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.security as security
from utils.security import create_reset_token, verify_reset_token, hash_password, verify_password

JWT_TEST_SECRET = "test-only-secret-not-for-deployment"


@pytest.fixture(autouse=True)
def configure_streamlit_secrets(monkeypatch):
    monkeypatch.setattr(
        security,
        "st",
        SimpleNamespace(secrets={"JWT_SECRET": JWT_TEST_SECRET}),
    )

def test_jwt_reset_token_full_cycle():
    """
    Verifies that the JWT token generation and verification cycle is 
    cryptographically sound and stable.
    """
    email = "test@student.edu"
    
    # 1. Generate Token
    token = create_reset_token(email)
    assert isinstance(token, str)
    assert len(token) > 20
    
    # 2. Verify Valid Token
    verified_email = verify_reset_token(token)
    assert verified_email == email

def test_jwt_expired_token():
    """
    Ensures the system correctly identifies and rejects expired 
    security tokens.
    """
    email = "expired@example.com"
    
    # Generate token that expires in 1 second
    token = create_reset_token(email, expires_in_minutes=0.016)  # ~1 second
    
    # Wait for expiration
    time.sleep(2)
    
    # Verify (should fail)
    assert verify_reset_token(token) is None

def test_jwt_corrupted_token():
    """
    Verifies that tampered or invalid tokens are identified and 
    rejected by the security layer.
    """
    token = "this.is.not.a.valid.jwt.token"
    assert verify_reset_token(token) is None
    
    # Tampered token (Valid format but wrong signature)
    valid_token = create_reset_token("test@test.com")
    tampered_token = valid_token[:-5] + "XXXXX"
    assert verify_reset_token(tampered_token) is None

def test_password_hashing_stability():
    """
    Verifies the integrity of the BCrypt hashing and verification logic.
    """
    plain = "SuperSecurePass123!"
    hashed = hash_password(plain)
    
    assert hashed != plain
    assert "$2b$" in hashed  # Check for BCrypt prefix
    
    # Correct verify
    assert verify_password(plain, hashed) is True
    
    # Incorrect verify
    assert verify_password("wrong_pass", hashed) is False

def test_jwt_token_payload_integrity():
    """
    Ensures the underlying JWT payload contains the required security claims.
    """
    email = "audit@security.com"
    token = create_reset_token(email)
    
    decoded = jwt.decode(token, JWT_TEST_SECRET, algorithms=["HS256"])
    assert decoded["email"] == email
    assert "exp" in decoded


@pytest.mark.parametrize("secrets", [{}, {"JWT_SECRET": ""}])
def test_jwt_secret_must_be_configured(monkeypatch, secrets):
    monkeypatch.setattr(security, "st", SimpleNamespace(secrets=secrets))

    with pytest.raises(RuntimeError, match="Set JWT_SECRET in Streamlit secrets"):
        create_reset_token("test@student.edu")
