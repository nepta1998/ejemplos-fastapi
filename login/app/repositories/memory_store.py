class InMemoryUserStore:
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}

    def get_by_email(self, email: str) -> dict | None:
        return self._users.get(email.lower())

    def create_user(self, email: str, password_hash: str) -> dict:
        key = email.lower()
        user = {"email": key, "password_hash": password_hash}
        self._users[key] = user
        return user
