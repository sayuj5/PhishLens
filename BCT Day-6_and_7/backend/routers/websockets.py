from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

from backend.logger import api_logger
from backend.discovery.events import bus

router = APIRouter(prefix="/api/ws", tags=["websockets"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        api_logger.info(f"WebSocket connected. Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            api_logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except RuntimeError:
                # Connection might be dropped
                self.disconnect(connection)

manager = ConnectionManager()

# Subscriber callback wrapper
async def on_discovery_event(data: dict):
    await manager.broadcast(data)

# Register the event bus subscriber
bus.subscribe("discovery_progress", on_discovery_event)
bus.subscribe("discovery_complete", on_discovery_event)

@router.websocket("/discovery")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect messages from client for now, just listening
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
