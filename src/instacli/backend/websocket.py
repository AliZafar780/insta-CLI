from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, Depends, WebSocket

from instacli.backend.app import get_service
from instacli.config import AppConfig
from instacli.services.insta_service import InstaService

logger = logging.getLogger(__name__)

websocket_router = APIRouter()


@websocket_router.websocket("/ws/notifications")
async def notifications_socket(
    websocket: WebSocket,
    service: InstaService = Depends(get_service),
):
    await websocket.accept()

    # Read the first message as an authentication token
    try:
        auth_data = await asyncio.wait_for(websocket.receive_json(), timeout=10.0)
        token = auth_data.get("token", "")
        configured_key = AppConfig.from_env().api_key
        if configured_key is None or token != configured_key:
            await websocket.close(code=4001)
            logger.warning("WebSocket connection rejected: invalid or missing auth token")
            return
    except asyncio.TimeoutError:
        await websocket.close(code=4001)
        logger.warning("WebSocket connection rejected: auth token timeout")
        return
    except Exception:
        await websocket.close(code=4001)
        logger.exception("WebSocket connection rejected: error during auth")
        return

    try:
        while True:
            _, digest = await service.notifications()
            await websocket.send_json({"digest": digest})
            await asyncio.sleep(5)
    except Exception:
        logger.exception("WebSocket notification loop error")
        await websocket.close()
