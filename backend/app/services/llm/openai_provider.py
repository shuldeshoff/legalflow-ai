from typing import AsyncIterator
import openai
from openai import AsyncOpenAI
import tiktoken
from app.core.config import settings
from app.services.llm.base_provider import BaseLLMProvider
from app.schemas.llm import ChatRequest, ChatResponse, StreamChunk, LLMProvider
import logging

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM Provider"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Generate chat completion"""
        try:
            response = await self.client.chat.completions.create(
                model=request.model.value,
                messages=[
                    {"role": msg.role.value, "content": msg.content}
                    for msg in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=False,
            )
            
            return ChatResponse(
                content=response.choices[0].message.content or "",
                model=request.model.value,
                provider=LLMProvider.OPENAI,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                },
                finish_reason=response.choices[0].finish_reason or "stop",
            )
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise
    
    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[StreamChunk]:
        """Stream chat completion"""
        try:
            stream = await self.client.chat.completions.create(
                model=request.model.value,
                messages=[
                    {"role": msg.role.value, "content": msg.content}
                    for msg in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield StreamChunk(
                        content=chunk.choices[0].delta.content,
                        done=False,
                    )
            
            # Final chunk
            yield StreamChunk(content="", done=True)
            
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))

