import pytest
from unittest.mock import patch
from app.schemas.user import UserResponse

@pytest.mark.asyncio
async def test_get_current_user_unauthorized(async_client):
    # Without token, it should fail
    response = await async_client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_authorized(async_client):
    # Mocking the dependency directly can be done via app.dependency_overrides
    from app.api.deps import get_current_active_user
    from app.models.user import User
    from app.main import app
    
    mock_user = User(
        id=1, 
        email="test@example.com", 
        full_name="Test User", 
        is_active=True,
        is_superuser=False
    )
    
    async def override_get_current_active_user():
        return mock_user
        
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    
    response = await async_client.get("/api/v1/users/me")
    
    # Clean up override
    app.dependency_overrides.pop(get_current_active_user)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
