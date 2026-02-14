from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import ENV_PATH
from .security.config import AuthSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_CACHE_DB: int
    REDIS_RATE_LIMITER_DB: int
    
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    
    S3_CLIENT_ACCESS_KEY: str
    S3_CLIENT_SECRET_KEY: str
    S3_CLIENT_ENDPOINT_URL: str
    S3_BUCKET_NAME: str
    
    GITHUB_OAUTH_CLIENT_ID: str
    GITHUB_OAUTH_CLIENT_SECRET: str
    
    REDIRECT_ENCRYPTION_KEY: str
    
    auth: AuthSettings = AuthSettings()
    
    model_config = SettingsConfigDict(env_file=ENV_PATH)
    
    @property
    def database_url_async(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def database_url_sync(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    
settings = Settings()