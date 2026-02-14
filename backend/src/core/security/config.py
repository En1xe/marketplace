from pathlib import Path
from pydantic import BaseModel

from core.constants import AUTH_PRIVATE_KEY_PATH, AUTH_PUBLIC_KEY_PATH


class AuthSettings(BaseModel):
    PRIVATE_KEY: Path = AUTH_PRIVATE_KEY_PATH
    PUBLIC_KEY: Path = AUTH_PUBLIC_KEY_PATH
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 30