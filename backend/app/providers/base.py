from abc import ABC, abstractmethod
from typing import Any


class BaseProvider(ABC):
    """Abstract base class for AI/LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier."""
        pass

    @abstractmethod
    async def generate(self, prompt: str, **kwargs: Any) -> str:
        """Generate response from provider."""
        pass

    @abstractmethod
    async def chat(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        """Handle chat conversation."""
        pass
