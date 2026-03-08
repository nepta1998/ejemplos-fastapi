from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    secret: str
    algorithm: str
    access_token_expire_minutes: int


def get_settings() -> Settings:
    return Settings(
        secret=os.getenv("APP_SECRET", "change-me-in-production"),
        algorithm=os.getenv("APP_ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    )
