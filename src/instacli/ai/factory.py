from __future__ import annotations

import os

from instacli.ai.base import AIProvider
from instacli.ai.providers import AnthropicProvider, NoAIProvider, OllamaProvider, OpenAIProvider


class AIProviderFactory:
    @staticmethod
    def build(provider: str) -> AIProvider:
        provider = provider.lower()
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            return OpenAIProvider(api_key=api_key)
        if provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY", "")
            return AnthropicProvider(api_key=api_key)
        if provider == "ollama":
            host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            return OllamaProvider(host=host)
        return NoAIProvider()

    @staticmethod
    async def safe_call(call, fallback):
        try:
            return await call
        except Exception:
            return fallback
