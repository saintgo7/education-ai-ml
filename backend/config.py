#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./education_platform.db"
    )

    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-this-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Education AI/ML Platform"
    PROJECT_DESCRIPTION: str = "Comprehensive learning platform with 668+ projects"

    # CORS
    CORS_ORIGINS: list = ["*"]

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
