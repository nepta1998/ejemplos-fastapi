# Ejemplo WebSocket con FastAPI

## Ejecutar con el comando `fastapi`

Desde esta carpeta:

```bash
poetry run fastapi dev app/main.py
```

Luego abre:

- <http://127.0.0.1:8000/chat>

## Endpoints

- `GET /chat` página del chat
- `WS /chat/ws` websocket del chat
