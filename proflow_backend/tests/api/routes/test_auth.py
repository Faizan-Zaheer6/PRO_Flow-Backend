import pytest
from unittest.mock import patch
from app.schemas.token import Token

@pytest.mark.asyncio
async def test_login_success(async_client):
    # Mock the auth service to bypass real DB check and password hashing
    mock_token = Token(access_token="mock_token", token_type="bearer")
    
    with patch("app.api.routes.auth.auth_service.authenticate_user", return_value=mock_token) as mock_auth:
        response = await async_client.post(
            "/api/v1/auth/login",
            data={"username": "test@example.com", "password": "password123"}
        )
        
        assert response.status_code == 200
        assert response.json() == {"access_token": "mock_token", "token_type": "bearer"}
        mock_auth.assert_called_once()
