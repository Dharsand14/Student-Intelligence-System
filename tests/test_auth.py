import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.users_db import add_user, get_user, delete_user
from utils.security import verify_password, hash_password

def test_password_hashing():
    password = "MySecurePassword123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_user_creation_and_auth():
    username = "testuser@edu.com"
    password = "TestPassWord789"
    role = "student"
    
    # Ensure user doesn't exist
    delete_user(username)
    
    # Create user
    add_user(username, password, role)
    
    # Retrieve and verify
    user = get_user(username)
    assert user is not None
    assert user["username"] == username
    assert user["role"] == role
    assert verify_password(password, user["password"]) is True
    
    # Clean up
    delete_user(username)
    assert get_user(username) is None

def test_duplicate_user_fails():
    username = "duplicate@edu.com"
    delete_user(username)
    
    add_user(username, "pass", "staff")
    
    # Should raise ValueError because user exists
    with pytest.raises(ValueError, match="User already exists"):
        add_user(username, "pass2", "student")
        
    delete_user(username)

if __name__ == "__main__":
    test_password_hashing()
    test_user_creation_and_auth()
    test_duplicate_user_fails()
    print("Authentication tests passed!")
