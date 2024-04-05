from fastapi import FastAPI, Depends
import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware
from .dependencies.auth import login_required
import uvicorn
import logging
import logging.config
import sys
from .middlewares import LoggingMiddleware
from .settings import settings

from .endpoints import posts
from .endpoints import auth
from .endpoints import profile
from .endpoints import parser
from .endpoints import internal

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

logging_config = {
    "version": 1,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stderr,
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"], "propagate": True},
}

logging.config.dictConfig(logging_config)

app = FastAPI(name="Arkive Web Service", debug=True)

app.add_middleware(
    LoggingMiddleware,
    logger=logging.getLogger(__name__),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(profile.router, dependencies=[Depends(login_required)])
app.include_router(parser.router)
app.include_router(internal.router)


def main():
    uvicorn.run(
        "arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True
    )
