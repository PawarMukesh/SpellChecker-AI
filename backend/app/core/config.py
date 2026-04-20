from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    def __init__(self) -> None:
        cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
        self.app_name = "enterprise-writing-assistant"
        self.model_name = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-0.5B-Instruct")
        self.model_server_url = os.getenv(
            "MODEL_SERVER_URL", "http://localhost:8001/v1/completions"
        )
        self.model_timeout_seconds = int(os.getenv("MODEL_TIMEOUT_SECONDS", "15"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.cors_origins = [
            origin.strip() for origin in cors_origins.split(",") if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
