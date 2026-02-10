from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


@dataclass(slots=True)
class Database:
    url: str

    def __post_init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(self.url, echo=False)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def init_models(self, base) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
