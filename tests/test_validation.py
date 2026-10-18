import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.validation import (
    is_valid_email,
    is_valid_phone,
    is_strong_password,
    is_valid_name,
    is_valid_student_id
)

def test_email_validation():
    assert is_valid_email("test@gmail.com") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("user@domain.co.uk") is True
    assert is_valid_email("") is False

def test_phone_validation():
    assert is_valid_phone("1234567890") is True
    assert is_valid_phone("12345") is False
    assert is_valid_phone("abcdefghij") is False
    assert is_valid_phone("12345678901") is False

def test_password_strength():
    # Pass: 8+ chars, upper, lower, digit, special
    assert is_strong_password("Secure@123") is True
    
    # Fail cases
    assert is_strong_password("short") is False
    assert is_strong_password("NoSpecial123") is False
    assert is_strong_password("nouppercase@1") is False
    assert is_strong_password("NOLOWERCASE@1") is False
    assert is_strong_password("NoDigiit@") is False

def test_name_validation():
    assert is_valid_name("John Doe") is True
    assert is_valid_name("Jo") is False # Min 3 chars
    assert is_valid_name("John123") is False # No digits

def test_student_id_validation():
    assert is_valid_student_id("S12345") is True
    assert is_valid_student_id("ID") is False # too short
    assert is_valid_student_id("ThisIDIsWayTooLongToBeValid12345") is False
    assert is_valid_student_id("STU-001") is True

from utils.validation import sanitize_text

def test_sanitization():
    # Test valid string
    assert sanitize_text("John Doe") == "John Doe"
    # Test HTML stripping
    assert sanitize_text("<b>Malicious!</b>") == "Malicious!"
    # Test script blocking
    assert sanitize_text("<script>alert(1)</script>") == "alert(1)"
    # Test javascript check
    assert sanitize_text("javascript:alert('hi')") == "#alert('hi')"

from utils.validation import is_valid_linkedin

def test_linkedin_validation():
    assert is_valid_linkedin("https://www.linkedin.com/in/johndoe") is True
    assert is_valid_linkedin("linkedin.com/in/johndoe") is False # No protocol
    assert is_valid_linkedin("https://facebook.com/johndoe") is False
    assert is_valid_linkedin("https://www.linkedin.com/in/john-doe_123/") is True

if __name__ == "__main__":
    test_email_validation()
    test_phone_validation()
    test_password_strength()
    test_name_validation()
    test_student_id_validation()
    test_sanitization()
    test_linkedin_validation()
    print("Validation tests with LinkedIn passed!")
