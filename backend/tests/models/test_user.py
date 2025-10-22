import pytest
from app.models.user import User


def test_create_user(db):
    """Test user model creation"""
    from app.core.security import get_password_hash
    
    user = User(
        email="test@example.com",
        full_name="Test User",
        is_active=True
    )
    user.password_hash = get_password_hash("testpassword")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active == True
    assert user.created_at is not None


def test_user_unique_email(db):
    """Test user email uniqueness constraint"""
    from app.core.security import get_password_hash
    
    user1 = User(email="duplicate@example.com", full_name="User 1", is_active=True)
    user1.password_hash = get_password_hash("password1")
    db.add(user1)
    db.commit()
    
    user2 = User(email="duplicate@example.com", full_name="User 2", is_active=True)
    user2.password_hash = get_password_hash("password2")
    db.add(user2)
    
    with pytest.raises(Exception):  # Should raise IntegrityError
        db.commit()
