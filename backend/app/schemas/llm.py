from enum import Enum
from typing import List, Optional, AsyncIterator
from pydantic import BaseModel


class LLMProvider(str, Enum):
    OPENAI = "openai"
    YANDEX = "yandex"


class LLMModel(str, Enum):
    # OpenAI
    GPT_4_TURBO = "gpt-4-turbo-preview"
    GPT_4 = "gpt-4"
    GPT_35_TURBO = "gpt-3.5-turbo"
    
    # Yandex
    YANDEX_GPT = "yandexgpt"
    YANDEX_GPT_LITE = "yandexgpt-lite"


class MessageRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    model: LLMModel = LLMModel.GPT_35_TURBO
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000
    stream: bool = False


class ChatResponse(BaseModel):
    content: str
    model: str
    provider: LLMProvider
    usage: dict
    finish_reason: str


class StreamChunk(BaseModel):
    content: str
    done: bool

