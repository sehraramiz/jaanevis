import pathlib
from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator

import jaanevis


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_URL: str
    API_V1_STR: str = "/api/v1"
    BASE_DIR = pathlib.PurePath(jaanevis.__file__).parent
    DATA_BASE_DIR = pathlib.PurePath(jaanevis.__file__).parent.parent
    CORS_ORIGINS: list[AnyHttpUrl] | str = []
    LANGUAGE_CODE: str = "en"

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

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
