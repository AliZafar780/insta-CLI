from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class AIProvider(Protocol):
    name: str

    async def summarize(self, text: str) -> str:
        ...

    async def generate_caption(self, context: str) -> str:
        ...

    async def moderate(self, text: str) -> bool:
        ...

    async def digest_notifications(self, text: str) -> str:
        ...


@dataclass(slots=True)
class AIResult:
    content: str
    provider: str
