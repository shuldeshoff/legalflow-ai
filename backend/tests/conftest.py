import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.config import settings

# Import all models to ensure they're registered
from app.models.user import User
from app.models.client import Client
from app.models.document import Document
from app.models.knowledge_base import KnowledgeBase
from app.models.integration import Integration, IntegrationLog, TelegramChat, Payment

# Test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Setup test database once for all tests"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a new database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


def override_get_db():
    """Override database dependency"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest_asyncio.fixture
async def client(db):
    """Async HTTP client for testing"""
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    from app.core.security import get_password_hash
    
    # Get the actual User model to check its fields
    from sqlalchemy import inspect
    from app.models.user import User
    
    mapper = inspect(User)
    columns = [col.key for col in mapper.columns]
    
    user = User(
        email="test@example.com",
        is_active=True,
        full_name="Test User"  # full_name is required
    )
    
    # Set password field based on actual model
    if 'hashed_password' in columns:
        user.hashed_password = get_password_hash("testpassword123")
    elif 'password_hash' in columns:
        user.password_hash = get_password_hash("testpassword123")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create auth headers with JWT token"""
    from app.core.security import create_access_token
    
    token = create_access_token({"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}
