from dataclasses import dataclass, asdict


@dataclass
class User:
    email: str
    password_hash: str

    def to_dict(self) -> dict:
        return asdict(self)
