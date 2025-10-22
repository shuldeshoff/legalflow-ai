from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.llm import ChatRequest, ChatResponse, LLMModel
from app.services.llm.llm_service import llm_service
from app.services.llm.prompts import get_system_prompt
from app.schemas.llm import Message, MessageRole
from app.api.deps import get_current_user
from app.models.user import User
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Chat with LLM
    
    Supports multiple models:
    - OpenAI: gpt-4-turbo-preview, gpt-4, gpt-3.5-turbo
    - Yandex: yandexgpt, yandexgpt-lite
    """
    try:
        # Add system prompt if not present
        if not request.messages or request.messages[0].role != MessageRole.SYSTEM:
            system_message = Message(
                role=MessageRole.SYSTEM,
                content=get_system_prompt("legal_assistant")
            )
            request.messages.insert(0, system_message)
        
        response = await llm_service.chat(request)
        return response
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Stream chat with LLM
    
    Returns Server-Sent Events (SSE) stream
    """
    try:
        # Add system prompt if not present
        if not request.messages or request.messages[0].role != MessageRole.SYSTEM:
            system_message = Message(
                role=MessageRole.SYSTEM,
                content=get_system_prompt("legal_assistant")
            )
            request.messages.insert(0, system_message)
        
        request.stream = True
        
        async def event_generator():
            try:
                async for chunk in llm_service.stream_chat(request):
                    yield f"data: {json.dumps(chunk.model_dump())}\n\n"
            except Exception as e:
                logger.error(f"Stream error: {e}")
                error_chunk = {"content": "", "done": True, "error": str(e)}
                yield f"data: {json.dumps(error_chunk)}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            },
        )
    
    except Exception as e:
        logger.error(f"Chat stream error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available models"""
    return {
        "models": [
            {
                "id": LLMModel.GPT_4_TURBO.value,
                "provider": "openai",
                "name": "GPT-4 Turbo",
                "description": "Most capable model, best for complex tasks",
            },
            {
                "id": LLMModel.GPT_4.value,
                "provider": "openai",
                "name": "GPT-4",
                "description": "Powerful model for most tasks",
            },
            {
                "id": LLMModel.GPT_35_TURBO.value,
                "provider": "openai",
                "name": "GPT-3.5 Turbo",
                "description": "Fast and cost-effective",
            },
            {
                "id": LLMModel.YANDEX_GPT.value,
                "provider": "yandex",
                "name": "YandexGPT",
                "description": "Yandex language model",
            },
            {
                "id": LLMModel.YANDEX_GPT_LITE.value,
                "provider": "yandex",
                "name": "YandexGPT Lite",
                "description": "Faster Yandex model",
            },
        ]
    }

