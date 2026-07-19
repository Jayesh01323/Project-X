from pydantic import BaseModel
from typing import Optional


class ProviderConfig(BaseModel):
    model: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_output_tokens: int = 1024


class ChatMessage(BaseModel):
    role: str
    content: str


class GenerateRequest(BaseModel):
    prompt: str
    config: Optional[ProviderConfig] = None


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    config: Optional[ProviderConfig] = None


class GenerateResponse(BaseModel):
    text: str


class ChatResponse(BaseModel):
    text: str
