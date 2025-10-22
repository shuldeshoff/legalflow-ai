import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import status


@pytest.mark.asyncio
async def test_chat_with_llm(client, auth_headers):
    """Test chat endpoint with LLM"""
    with patch('app.services.llm.llm_service.chat') as mock_chat:
        mock_response = Mock()
        mock_response.content = "Test response"
        mock_response.model = "gpt-3.5-turbo"
        mock_response.usage = {"total_tokens": 100}
        mock_chat.return_value = mock_response
        
        response = client.post(
            "/api/v1/llm/chat",
            headers=auth_headers,
            json={
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "model": "gpt-3.5-turbo"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "content" in data


def test_chat_unauthorized(client):
    """Test chat without authorization"""
    response = client.post(
        "/api/v1/llm/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "gpt-3.5-turbo"
        }
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_models(client, auth_headers):
    """Test getting available LLM models"""
    response = client.get(
        "/api/v1/llm/models",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0

