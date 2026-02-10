from __future__ import annotations

import asyncio
from dataclasses import dataclass

from instacli.ai.base import AIProvider


@dataclass(slots=True)
class NoAIProvider:
    name: str = "none"

    async def summarize(self, text: str) -> str:
        return "Summary unavailable (AI disabled)."

    async def generate_caption(self, context: str) -> str:
        return ""

    async def moderate(self, text: str) -> bool:
        return True

    async def digest_notifications(self, text: str) -> str:
        return "Notifications summary unavailable (AI disabled)."


@dataclass(slots=True)
class OpenAIProvider:
    api_key: str
    model: str = "gpt-4o-mini"
    name: str = "openai"

    async def summarize(self, text: str) -> str:
        return await self._request(f"Summarize this post: {text}")

    async def generate_caption(self, context: str) -> str:
        return await self._request(f"Generate a short caption: {context}")

    async def moderate(self, text: str) -> bool:
        response = await self._request(f"Is this content safe? {text}")
        return "yes" in response.lower()

    async def digest_notifications(self, text: str) -> str:
        return await self._request(f"Summarize notifications: {text}")

    async def _request(self, prompt: str) -> str:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("OpenAI SDK not installed") from exc

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text.strip()


@dataclass(slots=True)
class AnthropicProvider:
    api_key: str
    model: str = "claude-3-5-sonnet-20241022"
    name: str = "anthropic"

    async def summarize(self, text: str) -> str:
        return await self._request(f"Summarize this post: {text}")

    async def generate_caption(self, context: str) -> str:
        return await self._request(f"Generate a short caption: {context}")

    async def moderate(self, text: str) -> bool:
        response = await self._request(f"Is this content safe? {text}")
        return "yes" in response.lower()

    async def digest_notifications(self, text: str) -> str:
        return await self._request(f"Summarize notifications: {text}")

    async def _request(self, prompt: str) -> str:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("Anthropic SDK not installed") from exc

        client = anthropic.AsyncAnthropic(api_key=self.api_key)
        message = await client.messages.create(
            model=self.model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text.strip()


@dataclass(slots=True)
class OllamaProvider:
    host: str
    model: str = "llama3"
    name: str = "ollama"

    async def summarize(self, text: str) -> str:
        return await self._request(f"Summarize this post: {text}")

    async def generate_caption(self, context: str) -> str:
        return await self._request(f"Generate a short caption: {context}")

    async def moderate(self, text: str) -> bool:
        response = await self._request(f"Is this content safe? {text}")
        return "yes" in response.lower()

    async def digest_notifications(self, text: str) -> str:
        return await self._request(f"Summarize notifications: {text}")

    async def _request(self, prompt: str) -> str:
        try:
            import ollama
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("Ollama SDK not installed") from exc

        response = await asyncio.to_thread(
            ollama.generate,
            model=self.model,
            prompt=prompt,
            host=self.host,
        )
        return response.get("response", "").strip()
