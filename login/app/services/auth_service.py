import re

from passlib.context import CryptContext

from app.repositories.user_store import get_user_store

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_BCRYPT_BYTES = 72


class AuthService:
    def __init__(self) -> None:
        self.store = get_user_store()

    def register(self, email: str, password: str) -> dict:
        normalized_email = (email or "").strip().lower()
        if not EMAIL_RE.match(normalized_email):
            raise ValueError("Correo inválido")
        if not password:
            raise ValueError("La contraseña es obligatoria")
        if len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
            raise ValueError("La contraseña es demasiado larga (máximo 72 bytes para bcrypt)")
        if self.store.get_by_email(normalized_email):
            raise ValueError("Este correo ya está registrado")

        password_hash = pwd_context.hash(password)
        return self.store.create_user(normalized_email, password_hash)

    def authenticate(self, email: str, password: str) -> dict | None:
        normalized_email = (email or "").strip().lower()
        user = self.store.get_by_email(normalized_email)
        if not user:
            return None
        if not password or len(password.encode("utf-8")) > MAX_BCRYPT_BYTES:
            return None
        if not pwd_context.verify(password, user["password_hash"]):
            return None
        return user
