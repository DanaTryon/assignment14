from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional, List
import os
import sys

class Settings(BaseSettings):
    # Database settings (default if no env file is loaded)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/fastapi_db"
    
    # JWT Settings
    JWT_SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    JWT_REFRESH_SECRET_KEY: str = "your-refresh-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    BCRYPT_ROUNDS: int = 12
    CORS_ORIGINS: List[str] = ["*"]
    
    # Redis (optional, for token blacklisting)
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"
    
    class Config:
        # Decide which env file to load
        if "pytest" in sys.modules or os.getenv("ENV") == "test":
            env_file = ".env.test"
        else:
            env_file = ".env.development"
        case_sensitive = True

# Create a global settings instance
settings = Settings()

@lru_cache()
def get_settings() -> Settings:
    return Settings()
