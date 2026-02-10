from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol


@dataclass(slots=True)
class PostItem:
    id: str
    author: str
    caption: str
    media_url: str
    created_at: datetime


@dataclass(slots=True)
class ProfileItem:
    username: str
    display_name: str
    bio: str
    followers: int
    following: int
    posts: int


@dataclass(slots=True)
class NotificationItem:
    id: str
    title: str
    body: str
    created_at: datetime


class InstagramClient(Protocol):
    async def get_feed(self, cursor: int = 0) -> list[PostItem]:
        ...

    async def get_post(self, post_id: str) -> PostItem:
        ...

    async def get_profile(self) -> ProfileItem:
        ...

    async def search(self, query: str) -> list[PostItem]:
        ...

    async def get_notifications(self) -> list[NotificationItem]:
        ...

    async def create_post(self, caption: str, media_url: str) -> PostItem:
        ...


@dataclass(slots=True)
class MockInstagramClient:
    async def get_feed(self, cursor: int = 0) -> list[PostItem]:
        await asyncio.sleep(0.1)
        return [
            PostItem(
                id=str(cursor + index),
                author=f"creator_{cursor + index}",
                caption=f"Mock caption {cursor + index}",
                media_url="https://example.com/media.jpg",
                created_at=datetime.utcnow() - timedelta(hours=index),
            )
            for index in range(1, 6)
        ]

    async def get_post(self, post_id: str) -> PostItem:
        await asyncio.sleep(0.05)
        return PostItem(
            id=post_id,
            author=f"creator_{post_id}",
            caption=f"Mock caption {post_id}",
            media_url="https://example.com/media.jpg",
            created_at=datetime.utcnow(),
        )

    async def get_profile(self) -> ProfileItem:
        await asyncio.sleep(0.05)
        return ProfileItem(
            username="focus_user",
            display_name="Focus User",
            bio="Living with intention.",
            followers=1280,
            following=312,
            posts=84,
        )

    async def search(self, query: str) -> list[PostItem]:
        await asyncio.sleep(0.05)
        return [
            PostItem(
                id=f"search-{query}-{index}",
                author=f"search_{index}",
                caption=f"Result {index} for {query}",
                media_url="https://example.com/search.jpg",
                created_at=datetime.utcnow() - timedelta(days=index),
            )
            for index in range(1, 4)
        ]

    async def get_notifications(self) -> list[NotificationItem]:
        await asyncio.sleep(0.05)
        return [
            NotificationItem(
                id=str(index),
                title="New follower",
                body=f"User_{index} started following you.",
                created_at=datetime.utcnow() - timedelta(minutes=index * 6),
            )
            for index in range(1, 6)
        ]

    async def create_post(self, caption: str, media_url: str) -> PostItem:
        await asyncio.sleep(0.05)
        return PostItem(
            id="new",
            author="focus_user",
            caption=caption,
            media_url=media_url,
            created_at=datetime.utcnow(),
        )


@dataclass(slots=True)
class GraphInstagramClient:
    access_token: str
    base_url: str = "https://graph.facebook.com/v18.0"

    async def get_feed(self, cursor: int = 0) -> list[PostItem]:
        raise NotImplementedError("Graph API feed retrieval not yet implemented")

    async def get_post(self, post_id: str) -> PostItem:
        raise NotImplementedError("Graph API post retrieval not yet implemented")

    async def get_profile(self) -> ProfileItem:
        raise NotImplementedError("Graph API profile retrieval not yet implemented")

    async def search(self, query: str) -> list[PostItem]:
        raise NotImplementedError("Graph API search not yet implemented")

    async def get_notifications(self) -> list[NotificationItem]:
        raise NotImplementedError("Graph API notifications not yet implemented")

    async def create_post(self, caption: str, media_url: str) -> PostItem:
        raise NotImplementedError("Graph API media upload not yet implemented")


class InstagramClientFactory:
    @staticmethod
    def build(mode: str) -> InstagramClient:
        mode = mode.lower()
        if mode == "live":
            token = ""
            return GraphInstagramClient(access_token=token)
        return MockInstagramClient()
