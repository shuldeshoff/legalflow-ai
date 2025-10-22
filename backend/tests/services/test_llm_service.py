import pytest
from app.services.llm.llm_service import LLMService


def test_llm_service_get_models():
    """Test getting available LLM models"""
    service = LLMService()
    result = service.get_models()
    
    assert "models" in result
    assert isinstance(result["models"], list)
    assert len(result["models"]) > 0
    
    # Check model structure
    for model in result["models"]:
        assert "id" in model
        assert "name" in model
        assert "provider" in model
