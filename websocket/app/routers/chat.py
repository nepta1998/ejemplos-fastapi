from typing import List

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["chat"])


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.get("/")
def root_redirect():
    return RedirectResponse(url="/chat")


@router.get("/chat")
def chat_page(request: Request):
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request,
        "chat.html",
        {"request": request},
    )


@router.websocket("/chat/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.broadcast("🟢 Un usuario se conectó al chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"💬 {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("🔴 Un usuario salió del chat")


@router.get("/health")
def health():
    return {"status": "ok"}
