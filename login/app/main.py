from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import auth, home
from app.security.login_manager import manager

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="FastAPI Login Demo")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.state.templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(auth.router)
app.include_router(home.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return RedirectResponse(url="/login?message=Debes+iniciar+sesión&kind=error")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(404)
async def not_found_handler(request: Request, _: HTTPException):
    # Permitir requests de assets sin redirigir para evitar bucles en login/styles
    if request.url.path.startswith("/static") or request.url.path == "/favicon.ico":
        return JSONResponse(status_code=404, content={"detail": "Not Found"})

    try:
        await manager(request)
    except HTTPException:
        return RedirectResponse(url="/login?message=Debes+iniciar+sesión&kind=error")

    return JSONResponse(status_code=404, content={"detail": "Not Found"})
