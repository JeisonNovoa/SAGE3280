from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore',  # Ignore extra fields from .env file
    )

    # Database
    DATABASE_URL: str = "postgresql://sage_user:sage_password@localhost:5432/sage3280_db"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # CORS - Allow frontend origins
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost",      # Frontend en puerto 80
        "http://localhost:80",   # Frontend en puerto 80 (explícito)
        "http://localhost:3000", # Desarrollo React/Vite
        "http://localhost:5173", # Desarrollo Vite
        "http://localhost:8000", # Backend API
        "http://127.0.0.1",      # Alternativa localhost
        "http://127.0.0.1:80",   # Alternativa localhost puerto 80
    ]

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins - allow * for development or parse list"""
        if isinstance(v, str):
            if v == "*":
                # In production with Render, we'll allow all origins for simplicity
                # In a real production environment, you'd want to specify exact domains
                return ["*"]
            # If it's a JSON string, parse it
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # If not JSON, split by comma
                return [item.strip() for item in v.split(',')]
        return v

    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: Union[List[str], str] = ["xlsx", "xls", "csv"]

    @field_validator('ALLOWED_EXTENSIONS', mode='before')
    @classmethod
    def parse_allowed_extensions(cls, v):
        """Parse allowed extensions from environment variables"""
        if isinstance(v, str):
            # If it's a JSON string, parse it
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # If not JSON, split by comma
                return [item.strip() for item in v.split(',')]
        return v

    # Application
    APP_NAME: str = "SAGE3280"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Sistema de Gestión APS - Resolución 3280"


settings = Settings()
