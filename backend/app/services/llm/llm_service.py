from typing import Optional, Dict
from redis.asyncio import Redis
from app.core.config import settings
from app.services.llm.base_provider import BaseLLMProvider
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.yandex_provider import YandexProvider
from app.schemas.llm import (
    ChatRequest,
    ChatResponse,
    StreamChunk,
    LLMModel,
    LLMProvider as LLMProviderEnum,
)
import hashlib
import json
import logging
from typing import AsyncIterator

logger = logging.getLogger(__name__)


class LLMService:
    """Main LLM service with caching and provider routing"""
    
    def __init__(self):
        self.providers: Dict[LLMProviderEnum, BaseLLMProvider] = {
            LLMProviderEnum.OPENAI: OpenAIProvider(),
            LLMProviderEnum.YANDEX: YandexProvider(),
        }
        self.redis: Optional[Redis] = None
        self.cache_ttl = 3600  # 1 hour
    
    async def init_redis(self):
        """Initialize Redis connection"""
        try:
            self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            self.redis = None
    
    def _get_provider(self, model: LLMModel) -> BaseLLMProvider:
        """Get provider for model"""
        if model in [LLMModel.GPT_4, LLMModel.GPT_4_TURBO, LLMModel.GPT_35_TURBO]:
            return self.providers[LLMProviderEnum.OPENAI]
        elif model in [LLMModel.YANDEX_GPT, LLMModel.YANDEX_GPT_LITE]:
            return self.providers[LLMProviderEnum.YANDEX]
        else:
            raise ValueError(f"Unknown model: {model}")
    
    def _generate_cache_key(self, request: ChatRequest) -> str:
        """Generate cache key for request"""
        # Create hash from messages and parameters
        content = json.dumps({
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
            "model": request.model.value,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }, sort_keys=True)
        
        return f"llm:cache:{hashlib.md5(content.encode()).hexdigest()}"
    
    async def _get_from_cache(self, key: str) -> Optional[ChatResponse]:
        """Get response from cache"""
        if not self.redis:
            return None
        
        try:
            cached = await self.redis.get(key)
            if cached:
                data = json.loads(cached)
                return ChatResponse(**data)
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
        
        return None
    
    async def _save_to_cache(self, key: str, response: ChatResponse):
        """Save response to cache"""
        if not self.redis:
            return
        
        try:
            await self.redis.setex(
                key,
                self.cache_ttl,
                response.model_dump_json(),
            )
        except Exception as e:
            logger.warning(f"Cache save error: {e}")
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Generate chat completion with caching"""
        # Try cache first (only for non-streaming requests)
        if not request.stream:
            cache_key = self._generate_cache_key(request)
            cached_response = await self._get_from_cache(cache_key)
            
            if cached_response:
                logger.info(f"Cache hit for {request.model}")
                return cached_response
        
        # Get provider and generate
        provider = self._get_provider(request.model)
        response = await provider.chat(request)
        
        # Cache response
        if not request.stream:
            await self._save_to_cache(cache_key, response)
        
        return response
    
    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[StreamChunk]:
        """Stream chat completion"""
        provider = self._get_provider(request.model)
        async for chunk in provider.stream_chat(request):
            yield chunk
    
    def count_tokens(self, text: str, model: LLMModel) -> int:
        """Count tokens for text"""
        provider = self._get_provider(model)
        return provider.count_tokens(text)
    
    def get_models(self):
        """Get list of available models"""
        models = []
        
        # OpenAI models
        models.extend([
            {"id": "gpt-4-turbo-preview", "name": "GPT-4 Turbo", "provider": "openai"},
            {"id": "gpt-4", "name": "GPT-4", "provider": "openai"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"},
        ])
        
        # Yandex models
        models.extend([
            {"id": "yandexgpt", "name": "YandexGPT", "provider": "yandex"},
            {"id": "yandexgpt-lite", "name": "YandexGPT Lite", "provider": "yandex"},
        ])
        
        return {"models": models}


# Global service instance
llm_service = LLMService()

