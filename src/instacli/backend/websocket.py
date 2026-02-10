from __future__ import annotations

import asyncio

from fastapi import APIRouter, Depends, WebSocket

from instacli.backend.app import get_service
from instacli.services.insta_service import InstaService

websocket_router = APIRouter()


@websocket_router.websocket("/ws/notifications")
async def notifications_socket(
    websocket: WebSocket,
    service: InstaService = Depends(get_service),
):
    await websocket.accept()
    try:
        while True:
            _, digest = await service.notifications()
            await websocket.send_json({"digest": digest})
            await asyncio.sleep(5)
    except Exception:
        await websocket.close()
