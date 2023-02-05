from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from jaanevis.config import settings
from jaanevis.i18n import translate

from .endpoints import router

app = FastAPI()

app.include_router(router, prefix=settings.API_V1_STR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def set_locale(request: Request, call_next):
    lang = request.headers.get("accept-language", "en")

    with translate(lang):
        response = await call_next(request)
        response.headers["Content-Language"] = lang
        return response
