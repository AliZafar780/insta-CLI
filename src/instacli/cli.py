from __future__ import annotations

from dataclasses import dataclass

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    LoadingIndicator,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
)

from instacli.ai.factory import AIProviderFactory
from instacli.config import AppConfig
from instacli.instagram.client import InstagramClientFactory
from instacli.services.insta_service import InstaService


@dataclass
class AppState:
    config: AppConfig
    service: InstaService
    feed_cursor: int = 0
    current_caption: str = ""
    last_summary: str = ""


class PostSelected(Message):
    def __init__(self, post_id: str) -> None:
        super().__init__()
        self.post_id = post_id


class FeedPane(Vertical):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.list_view = ListView()
        self.loading = LoadingIndicator()

    async def on_mount(self) -> None:
        await self.load_feed()

    def compose(self) -> ComposeResult:
        yield Label("Your mindful feed", classes="panel-title")
        yield self.loading
        yield self.list_view
        yield Button("Load more", id="load-more")

    async def load_feed(self) -> None:
        self.loading.display = True
        posts = await self.state.service.fetch_feed(self.state.feed_cursor)
        for post in posts:
            item = ListItem(
                Static(f"@{post.author} · {post.caption}"),
                id=post.id,
            )
            self.list_view.append(item)
        self.state.feed_cursor += len(posts)
        self.loading.display = False

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "load-more":
            await self.load_feed()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id:
            self.post_message(PostSelected(event.item.id))


class PostDetailPane(Vertical):
    post_id = reactive("")

    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.summary = Static("", classes="panel-summary")
        self.content = Static("Select a post to see details", classes="panel-body")

    def compose(self) -> ComposeResult:
        yield Label("Post spotlight", classes="panel-title")
        yield self.content
        yield self.summary

    async def show_post(self, post_id: str) -> None:
        post = await self.state.service.fetch_post(post_id)
        summary = await self.state.service.summarize(post.caption)
        self.content.update(f"@{post.author}\n{post.caption}\nMedia: {post.media_url}")
        self.summary.update(f"AI summary: {summary}")


class ProfilePane(Vertical):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.content = Static("", classes="panel-body")

    async def on_mount(self) -> None:
        profile = await self.state.service.fetch_profile()
        self.content.update(
            f"{profile.display_name} (@{profile.username})\n"
            f"{profile.bio}\n"
            f"Followers: {profile.followers} | Following: {profile.following}\n"
            f"Posts: {profile.posts}"
        )

    def compose(self) -> ComposeResult:
        yield Label("Profile & insights", classes="panel-title")
        yield self.content


class ComposePane(Vertical):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.caption_input = TextArea(id="caption")
        self.media_input = Input(placeholder="Media URL", id="media-url")
        self.ai_hint = Static("", classes="panel-summary")

    def compose(self) -> ComposeResult:
        yield Label("Compose intentionally", classes="panel-title")
        yield Label("Caption")
        yield self.caption_input
        yield Label("Media URL")
        yield self.media_input
        yield Horizontal(
            Button("AI assist", id="ai-caption"),
            Button("Publish", id="publish"),
            classes="button-row",
        )
        yield self.ai_hint

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ai-caption":
            context = self.caption_input.text
            caption = await self.state.service.generate_caption(context)
            if caption:
                self.caption_input.text = f"{context}\n{caption}".strip()
                self.ai_hint.update("AI suggestion added.")
            else:
                self.ai_hint.update("AI suggestion unavailable.")
        if event.button.id == "publish":
            caption = self.caption_input.text
            media_url = self.media_input.value
            post = await self.state.service.create_post(caption, media_url)
            self.ai_hint.update(f"Posted with id {post.id}")


class SearchPane(Vertical):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.query_input = Input(placeholder="Search for creators, topics")
        self.results = ListView()

    def compose(self) -> ComposeResult:
        yield Label("Search & explore", classes="panel-title")
        yield self.query_input
        yield Button("Search", id="search")
        yield self.results

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "search":
            return
        self.results.clear()
        query = self.query_input.value
        results = await self.state.service.search_posts(query)
        for post in results:
            self.results.append(ListItem(Static(f"@{post.author}: {post.caption}")))


class NotificationsPane(Vertical):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.digest = Static("", classes="panel-summary")
        self.items = ListView()

    async def on_mount(self) -> None:
        await self.refresh_notifications()

    def compose(self) -> ComposeResult:
        yield Label("Smart notifications", classes="panel-title")
        yield self.digest
        yield self.items
        yield Button("Refresh", id="refresh")

    async def refresh_notifications(self) -> None:
        self.items.clear()
        notifications, digest = await self.state.service.notifications()
        self.digest.update(digest)
        for item in notifications:
            self.items.append(ListItem(Static(f"{item.title}: {item.body}")))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh":
            await self.refresh_notifications()


class SettingsPane(Vertical):
    def __init__(self, state: AppState) -> None:
        super().__init__()
        self.state = state
        self.theme_label = Label("")
        self.mode_label = Label("")

    async def on_mount(self) -> None:
        self.theme_label.update(f"Theme: {self.state.config.theme}")
        self.mode_label.update(f"Instagram mode: {self.state.config.instagram_mode}")

    def compose(self) -> ComposeResult:
        yield Label("Settings & themes", classes="panel-title")
        yield self.theme_label
        yield self.mode_label
        yield Static("Toggle themes in your config.", classes="panel-body")


class InstaApp(App):
    CSS = """
    Screen { background: $surface; }
    .panel-title { text-style: bold; margin-bottom: 1; }
    .panel-summary { color: $primary-lighten-2; margin-top: 1; }
    .panel-body { margin-bottom: 1; }
    .button-row { margin-top: 1; }
    """

    BINDINGS = [
        ("f", "focus_tab('feed')", "Feed"),
        ("p", "focus_tab('profile')", "Profile"),
        ("c", "focus_tab('compose')", "Compose"),
        ("s", "focus_tab('search')", "Search"),
        ("n", "focus_tab('notifications')", "Notifications"),
        ("t", "focus_tab('settings')", "Settings"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        ai_provider = AIProviderFactory.build(config.ai_provider)
        instagram_client = InstagramClientFactory.build(config.instagram_mode)
        service = InstaService(ai_provider=ai_provider, instagram_client=instagram_client)
        self.state = AppState(config=config, service=service)
        self.dark = config.theme == "dark"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent(initial="feed"):
            with TabPane("Feed", id="feed"):
                yield FeedPane(self.state)
            with TabPane("Post", id="post"):
                yield PostDetailPane(self.state)
            with TabPane("Profile", id="profile"):
                yield ProfilePane(self.state)
            with TabPane("Compose", id="compose"):
                yield ComposePane(self.state)
            with TabPane("Search", id="search"):
                yield SearchPane(self.state)
            with TabPane("Notifications", id="notifications"):
                yield NotificationsPane(self.state)
            with TabPane("Settings", id="settings"):
                yield SettingsPane(self.state)
        yield Footer()

    def action_focus_tab(self, tab_id: str) -> None:
        tabbed = self.query_one(TabbedContent)
        tabbed.active = tab_id

    async def on_post_selected(self, message: PostSelected) -> None:
        tabbed = self.query_one(TabbedContent)
        tabbed.active = "post"
        post_pane = self.query_one(PostDetailPane)
        await post_pane.show_post(message.post_id)
