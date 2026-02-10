from __future__ import annotations

import os
from dataclasses import dataclass


def _get_env(key: str, default: str) -> str:
    return os.getenv(key, default)


@dataclass(frozen=True)
class AppConfig:
    database_url: str
    ai_provider: str
    instagram_mode: str
    theme: str
    api_host: str
    api_port: int
    api_key: str | None

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            database_url=_get_env(
                "INSTACLI_DATABASE_URL", "sqlite+aiosqlite:///./instacli.db"
            ),
            ai_provider=_get_env("INSTACLI_AI_PROVIDER", "none"),
            instagram_mode=_get_env("INSTACLI_INSTAGRAM_MODE", "mock"),
            theme=_get_env("INSTACLI_THEME", "dark"),
            api_host=_get_env("INSTACLI_API_HOST", "127.0.0.1"),
            api_port=int(_get_env("INSTACLI_API_PORT", "8000")),
            api_key=os.getenv("INSTACLI_API_KEY"),
        )
