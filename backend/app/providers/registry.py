from typing import Type
from app.providers.base import BaseProvider


class ProviderRegistry:
    """Registry for AI/LLM providers."""

    _providers: dict[str, Type[BaseProvider]] = {}

    @classmethod
    def register(cls, provider_class: Type[BaseProvider]) -> Type[BaseProvider]:
        """Register a provider class."""
        instance = provider_class()
        cls._providers[instance.name] = provider_class
        return provider_class

    @classmethod
    def get(cls, name: str) -> BaseProvider | None:
        """Get provider instance by name."""
        provider_class = cls._providers.get(name)
        if provider_class:
            return provider_class()
        return None

    @classmethod
    def list_providers(cls) -> list[str]:
        """List all registered provider names."""
        return list(cls._providers.keys())

    @classmethod
    def has_provider(cls, name: str) -> bool:
        """Check if provider is registered."""
        return name in cls._providers
