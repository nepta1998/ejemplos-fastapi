from typing import Protocol

from app.repositories.memory_store import InMemoryUserStore


class UserStore(Protocol):
    def get_by_email(self, email: str) -> dict | None:
        ...

    def create_user(self, email: str, password_hash: str) -> dict:
        ...


_store: UserStore | None = None


def get_user_store() -> UserStore:
    global _store
    if _store is None:
        _store = InMemoryUserStore()
    return _store


def reset_user_store() -> None:
    global _store
    _store = None
