from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from instacli.ai.factory import AIProviderFactory
from instacli.config import AppConfig
from instacli.data import Base, Database
from instacli.instagram.client import InstagramClientFactory
from instacli.services.insta_service import InstaService


def _get_service(app: FastAPI) -> InstaService:
    return app.state.service


def _auth_dependency(x_api_key: str | None = Header(default=None)) -> None:
    configured = AppConfig.from_env().api_key
    if configured is None:
        return
    if x_api_key != configured:
        raise HTTPException(status_code=401, detail="Invalid API key")


def build_app(config: AppConfig) -> FastAPI:
    app = FastAPI(title="InstaCLI Backend", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    database = Database(config.database_url)
    ai_provider = AIProviderFactory.build(config.ai_provider)
    instagram_client = InstagramClientFactory.build(config.instagram_mode)
    service = InstaService(ai_provider=ai_provider, instagram_client=instagram_client)
    app.state.database = database
    app.state.service = service

    from instacli.backend.routes import router
    from instacli.backend.websocket import websocket_router

    app.include_router(router, dependencies=[Depends(_auth_dependency)])
    app.include_router(websocket_router, dependencies=[Depends(_auth_dependency)])

    @app.on_event("startup")
    async def _startup() -> None:
        await database.init_models(Base)

    return app


def get_service(request: Request) -> InstaService:
    return _get_service(request.app)
