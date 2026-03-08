from datetime import timedelta

from fastapi_login import LoginManager

from app.core.config import get_settings
from app.repositories.user_store import get_user_store

settings = get_settings()
manager = LoginManager(
    settings.secret,
    token_url="/login",
    use_cookie=True,
    default_expiry=timedelta(minutes=settings.access_token_expire_minutes),
    cookie_name="access-token",
)


@manager.user_loader()
def load_user(email: str):
    store = get_user_store()
    return store.get_by_email(email)
