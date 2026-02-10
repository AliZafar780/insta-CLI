from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from instacli.backend.app import get_service
from instacli.services.insta_service import InstaService

router = APIRouter(prefix="/api")


class PostResponse(BaseModel):
    id: str
    author: str
    caption: str
    media_url: str
    created_at: datetime


class ProfileResponse(BaseModel):
    username: str
    display_name: str
    bio: str
    followers: int
    following: int
    posts: int


class NotificationResponse(BaseModel):
    id: str
    title: str
    body: str
    created_at: datetime


class ComposeRequest(BaseModel):
    caption: str
    media_url: str


class SearchRequest(BaseModel):
    query: str


@router.get("/feed", response_model=list[PostResponse])
async def feed(cursor: int = 0, service: InstaService = Depends(get_service)):
    posts = await service.fetch_feed(cursor)
    return [PostResponse(**post.__dict__) for post in posts]


@router.get("/posts/{post_id}", response_model=PostResponse)
async def post_detail(post_id: str, service: InstaService = Depends(get_service)):
    post = await service.fetch_post(post_id)
    return PostResponse(**post.__dict__)


@router.get("/profile", response_model=ProfileResponse)
async def profile(service: InstaService = Depends(get_service)):
    profile = await service.fetch_profile()
    return ProfileResponse(**profile.__dict__)


@router.post("/search", response_model=list[PostResponse])
async def search(payload: SearchRequest, service: InstaService = Depends(get_service)):
    results = await service.search_posts(payload.query)
    return [PostResponse(**post.__dict__) for post in results]


@router.get("/notifications", response_model=dict)
async def notifications(service: InstaService = Depends(get_service)):
    items, digest = await service.notifications()
    return {
        "digest": digest,
        "items": [NotificationResponse(**item.__dict__) for item in items],
    }


@router.post("/compose", response_model=PostResponse)
async def compose(payload: ComposeRequest, service: InstaService = Depends(get_service)):
    post = await service.create_post(payload.caption, payload.media_url)
    return PostResponse(**post.__dict__)
