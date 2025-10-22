import pytest
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)


def test_password_hashing():
    """Test password hashing"""
    password = "TestPassword123!"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 0


def test_password_verification():
    """Test password verification"""
    password = "TestPassword123!"
    hashed = get_password_hash(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_create_access_token():
    """Test JWT access token creation"""
    user_id = 123
    token = create_access_token({"sub": str(user_id)})
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token():
    """Test JWT refresh token creation"""
    user_id = 123
    token = create_refresh_token({"sub": str(user_id)})
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token():
    """Test JWT token decoding"""
    user_id = 123
    token = create_access_token({"sub": str(user_id)})
    payload = decode_token(token)
    
    assert payload is not None
    assert payload["sub"] == str(user_id)


def test_decode_invalid_token():
    """Test decoding invalid token"""
    invalid_token = "invalid.token.here"
    payload = decode_token(invalid_token)
    
    assert payload is None

