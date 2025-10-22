import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.llm.llm_service import LLMService
from app.schemas.llm import ChatRequest, Message, MessageRole, LLMModel


@pytest.mark.asyncio
async def test_llm_service_chat():
    """Test LLM service chat functionality"""
    service = LLMService()
    
    with patch.object(service, 'get_provider') as mock_get_provider:
        mock_provider = Mock()
        mock_response = Mock()
        mock_response.content = "Test response"
        mock_response.model = "gpt-3.5-turbo"
        mock_response.usage = {"total_tokens": 100}
        mock_provider.chat = AsyncMock(return_value=mock_response)
        mock_get_provider.return_value = mock_provider
        
        request = ChatRequest(
            messages=[
                Message(role=MessageRole.USER, content="Hello")
            ],
            model=LLMModel.GPT_35_TURBO
        )
        
        response = await service.chat(request)
        
        assert response.content == "Test response"
        assert response.model == "gpt-3.5-turbo"


@pytest.mark.asyncio
async def test_llm_service_get_models():
    """Test getting available LLM models"""
    service = LLMService()
    models = service.get_models()
    
    assert isinstance(models, list)
    assert len(models) > 0
    
    for model in models:
        assert "id" in model
        assert "name" in model
        assert "provider" in model

