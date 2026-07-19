from app.providers.registry import ProviderRegistry
from app.providers.base import BaseProvider


def create_provider(name: str) -> BaseProvider | None:
    """Create a provider instance by registered name."""
    return ProviderRegistry.get(name)
