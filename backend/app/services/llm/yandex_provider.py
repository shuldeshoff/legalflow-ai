from typing import AsyncIterator
import aiohttp
import logging
from app.core.config import settings
from app.services.llm.base_provider import BaseLLMProvider
from app.schemas.llm import ChatRequest, ChatResponse, StreamChunk, LLMProvider

logger = logging.getLogger(__name__)


class YandexProvider(BaseLLMProvider):
    """Yandex GPT Provider"""
    
    def __init__(self):
        self.api_key = settings.YANDEX_GPT_API_KEY
        self.folder_id = settings.YANDEX_FOLDER_ID
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1"
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Generate chat completion"""
        if not self.api_key or not self.folder_id:
            raise ValueError("Yandex GPT credentials not configured")
        
        try:
            model_uri = f"gpt://{self.folder_id}/{request.model.value}/latest"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/completion",
                    headers={
                        "Authorization": f"Api-Key {self.api_key}",
                        "x-folder-id": self.folder_id,
                    },
                    json={
                        "modelUri": model_uri,
                        "completionOptions": {
                            "temperature": request.temperature,
                            "maxTokens": request.max_tokens,
                        },
                        "messages": [
                            {"role": msg.role.value, "text": msg.content}
                            for msg in request.messages
                        ],
                    },
                ) as response:
                    data = await response.json()
                    
                    if response.status != 200:
                        raise Exception(f"Yandex GPT error: {data}")
                    
                    result = data["result"]
                    
                    return ChatResponse(
                        content=result["alternatives"][0]["message"]["text"],
                        model=request.model.value,
                        provider=LLMProvider.YANDEX,
                        usage={
                            "prompt_tokens": result["usage"]["inputTextTokens"],
                            "completion_tokens": result["usage"]["completionTokens"],
                            "total_tokens": result["usage"]["totalTokens"],
                        },
                        finish_reason=result["alternatives"][0].get("status", "stop"),
                    )
        except Exception as e:
            logger.error(f"Yandex GPT chat error: {e}")
            raise
    
    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[StreamChunk]:
        """Stream chat completion"""
        if not self.api_key or not self.folder_id:
            raise ValueError("Yandex GPT credentials not configured")
        
        try:
            model_uri = f"gpt://{self.folder_id}/{request.model.value}/latest"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/completionAsync",
                    headers={
                        "Authorization": f"Api-Key {self.api_key}",
                        "x-folder-id": self.folder_id,
                    },
                    json={
                        "modelUri": model_uri,
                        "completionOptions": {
                            "temperature": request.temperature,
                            "maxTokens": request.max_tokens,
                            "stream": True,
                        },
                        "messages": [
                            {"role": msg.role.value, "text": msg.content}
                            for msg in request.messages
                        ],
                    },
                ) as response:
                    async for line in response.content:
                        if line:
                            try:
                                import json
                                data = json.loads(line)
                                
                                if "result" in data:
                                    text = data["result"]["alternatives"][0]["message"]["text"]
                                    done = data["result"]["alternatives"][0].get("status") == "ALTERNATIVE_STATUS_FINAL"
                                    
                                    yield StreamChunk(content=text, done=done)
                                    
                                    if done:
                                        break
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"Yandex GPT stream error: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text (approximate)"""
        # Yandex uses similar tokenization to GPT, approximate 4 chars per token
        return len(text) // 4

