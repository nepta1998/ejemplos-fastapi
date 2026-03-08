from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.security.login_manager import manager
from app.services.auth_service import AuthService

router = APIRouter(tags=["auth"])
auth_service = AuthService()


def _render(request: Request, templates: Jinja2Templates, name: str, message: str = "", kind: str = ""):
    return templates.TemplateResponse(
        request,
        name,
        {"request": request, "message": message, "kind": kind},
    )


@router.get("/login")
def login_page(request: Request):
    templates: Jinja2Templates = request.app.state.templates
    message = request.query_params.get("message", "")
    kind = request.query_params.get("kind", "")
    return _render(request, templates, "login.html", message, kind)


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = auth_service.authenticate(email, password)
    templates: Jinja2Templates = request.app.state.templates

    if not user:
        return _render(request, templates, "login.html", "Credenciales inválidas", "error")

    access_token = manager.create_access_token(data={"sub": user["email"]})
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    manager.set_cookie(response, access_token)
    return response


@router.get("/register")
def register_page(request: Request):
    templates: Jinja2Templates = request.app.state.templates
    message = request.query_params.get("message", "")
    kind = request.query_params.get("kind", "")
    return _render(request, templates, "register.html", message, kind)


@router.post("/register")
def register(request: Request, email: str = Form(...), password: str = Form(...)):
    templates: Jinja2Templates = request.app.state.templates

    try:
        auth_service.register(email, password)
    except ValueError as exc:
        return _render(request, templates, "register.html", str(exc), "error")

    return RedirectResponse(
        url="/login?message=Usuario+creado,+ya+puedes+iniciar+sesión&kind=success",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/logout")
def logout():
    response = RedirectResponse(
        url="/login?message=Sesión+cerrada&kind=success",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    response.delete_cookie("access-token")
    return response
