import os
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr

import jaanevis


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_URL: str
    CORS_ORIGINS: list[AnyHttpUrl] = []
    BASE_DIR = os.path.dirname(os.path.realpath(jaanevis.__file__))

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
