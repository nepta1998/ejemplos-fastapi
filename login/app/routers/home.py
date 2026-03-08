from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from app.security.login_manager import manager

router = APIRouter(tags=["home"])


@router.get("/")
def root_redirect():
    return RedirectResponse(url="/login")


@router.get("/home")
def home(request: Request, user=Depends(manager)):
    templates = request.app.state.templates
    return templates.TemplateResponse(
        request,
        "home.html",
        {"request": request, "user": user},
    )


@router.get("/health")
def health():
    return {"status": "ok"}
