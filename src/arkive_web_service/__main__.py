from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .dependencies.auth import login_required
import uvicorn
import logging
import logging.config
import sys
from .middlewares import LoggingMiddleware

from .endpoints import posts
from .endpoints import auth
from .endpoints import profile
from .endpoints import parser

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

# TODO: move this origins to config later
origins = [
    "http://localhost",
    "http://localhost:5173",
    "*",
]


app = FastAPI(name="Arkive Web Service", debug=True)

app.add_middleware(
    LoggingMiddleware,
    logger=logging.getLogger(__name__),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(profile.router, dependencies=[Depends(login_required)])
app.include_router(parser.router)


def main():
    uvicorn.run(
        "arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True
    )
