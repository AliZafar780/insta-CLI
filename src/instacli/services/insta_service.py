from __future__ import annotations

from dataclasses import dataclass

from instacli.ai.base import AIProvider
from instacli.ai.factory import AIProviderFactory
from instacli.instagram.client import InstagramClient, NotificationItem, PostItem, ProfileItem


@dataclass(slots=True)
class InstaService:
    ai_provider: AIProvider
    instagram_client: InstagramClient

    async def fetch_feed(self, cursor: int = 0) -> list[PostItem]:
        posts = await self.instagram_client.get_feed(cursor)
        filtered = []
        for post in posts:
            is_safe = await AIProviderFactory.safe_call(
                self.ai_provider.moderate(post.caption),
                True,
            )
            if is_safe:
                filtered.append(post)
        return filtered

    async def fetch_post(self, post_id: str) -> PostItem:
        return await self.instagram_client.get_post(post_id)

    async def fetch_profile(self) -> ProfileItem:
        return await self.instagram_client.get_profile()

    async def search_posts(self, query: str) -> list[PostItem]:
        return await self.instagram_client.search(query)

    async def notifications(self) -> tuple[list[NotificationItem], str]:
        notifications = await self.instagram_client.get_notifications()
        digest_source = "\n".join(
            f"{item.title}: {item.body}" for item in notifications
        )
        digest = await AIProviderFactory.safe_call(
            self.ai_provider.digest_notifications(digest_source),
            "Notifications summary unavailable.",
        )
        return notifications, digest

    async def create_post(self, caption: str, media_url: str) -> PostItem:
        return await self.instagram_client.create_post(caption, media_url)

    async def summarize(self, text: str) -> str:
        return await AIProviderFactory.safe_call(
            self.ai_provider.summarize(text),
            "Summary unavailable.",
        )

    async def generate_caption(self, context: str) -> str:
        return await AIProviderFactory.safe_call(
            self.ai_provider.generate_caption(context),
            "",
        )
