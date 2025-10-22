import pytest
from app.models.user import User
from app.core.security import get_password_hash


def test_create_user(db):
    """Test user model creation"""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.created_at is not None


def test_user_unique_email(db):
    """Test user email uniqueness constraint"""
    user1 = User(
        email="duplicate@example.com",
        hashed_password=get_password_hash("password1")
    )
    db.add(user1)
    db.commit()
    
    user2 = User(
        email="duplicate@example.com",
        hashed_password=get_password_hash("password2")
    )
    db.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db.commit()

