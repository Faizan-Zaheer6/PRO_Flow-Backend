import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db
from unittest.mock import AsyncMock

# Mock DB session dependency
async def override_get_db():
    session = AsyncMock()
    yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
