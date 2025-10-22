from abc import ABC, abstractmethod
from typing import AsyncIterator
from app.schemas.llm import ChatRequest, ChatResponse, StreamChunk


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    @abstractmethod
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Generate chat completion"""
        pass
    
    @abstractmethod
    async def stream_chat(self, request: ChatRequest) -> AsyncIterator[StreamChunk]:
        """Stream chat completion"""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        pass

