from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project-X"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = "Project-X FastAPI Backend Foundation"
    
    # Database
    DATABASE_URL: str = "sqlite:///./project_x.db"
    
    # Security
    SECRET_KEY: str = "development-secret-key-change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # Frontend dev server
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Alternative frontend
        "chrome-extension://*",   # Extension
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
