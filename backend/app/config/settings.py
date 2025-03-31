import os
from typing import ClassVar
from pathlib import Path

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    WORKERS: int = int(os.getenv("WORKERS", 1))
    FORWARDED_ALLOW_IPS: str = os.getenv("FORWARDED_ALLOW_IPS", "*")
    KEEPALIVE: int = int(os.getenv("KEEPALIVE", 120))
    REDIS_DSN: str = os.getenv('REDIS_DSN', "redis://localhost:6380")
    DATABASE_DSN: str = os.getenv("DATABASE_DSN", "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", 2)) 
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "jwt123")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "1"))
    # YANDEX AUTH
    YANDEX_CLIENT_ID: str = os.getenv("YANDEX_CLIENT_ID", "53591c42b83f4b14b5e285c95d617aec")
    YANDEX_CLIENT_SECRET: str = os.getenv("YANDEX_CLIENT_SECRET", "bb7f16fcd8254fe19c2f056927174757")
    YANDEX_REDIRECT_URI: str = os.getenv("YANDEX_REDIRECT_URI", "http://localhost:8000/api/v1/auth/yandex/callback")
    # DIR
    UPLOAD_DIR: ClassVar[Path] = Path("app/uploads")
    UPLOAD_DIR.mkdir(exist_ok=True)
    # MODS 
    TEST_MODE: bool = bool(os.getenv("TEST_MODE", True))
    
    
settings = Settings()