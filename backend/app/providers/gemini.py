import os
from typing import Any
from app.providers.base import BaseProvider
from app.providers.registry import ProviderRegistry


@ProviderRegistry.register
class GeminiProvider(BaseProvider):
    """Google Gemini provider using google-genai SDK."""

    _name = "gemini"
    _model: str = "gemini-2.0-flash"

    @property
    def name(self) -> str:
        return self._name

    async def generate(self, prompt: str, **kwargs: Any) -> str:
        try:
            from google import genai

            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not configured")

            client = genai.Client(api_key=api_key)
            model = kwargs.get("model", self._model)
            response = await client.aio.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "temperature": kwargs.get("temperature", 0.7),
                    "max_output_tokens": kwargs.get("max_tokens", 1024),
                },
            )
            return response.text or ""

        except ImportError:
            raise ImportError(
                "google-genai SDK not installed. Install with: pip install google-genai"
            )
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}")

    async def chat(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        try:
            from google import genai

            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not configured")

            client = genai.Client(api_key=api_key)
            model = kwargs.get("model", self._model)

            contents = []
            for msg in messages:
                role = msg.get("role", "user")
                text = msg.get("content", "")
                role_mapped = "model" if role == "assistant" else "user"
                contents.append({"role": role_mapped, "parts": [{"text": text}]})

            response = await client.aio.models.generate_content(
                model=model,
                contents=contents,
                config={
                    "temperature": kwargs.get("temperature", 0.7),
                    "max_output_tokens": kwargs.get("max_tokens", 1024),
                },
            )
            return response.text or ""

        except ImportError:
            raise ImportError(
                "google-genai SDK not installed. Install with: pip install google-genai"
            )
        except Exception as e:
            raise RuntimeError(f"Gemini chat failed: {e}")
