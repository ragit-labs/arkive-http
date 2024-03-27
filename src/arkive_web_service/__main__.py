from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .endpoints import login
from .endpoints import posts
from .endpoints.auth import auth_router

# TODO: move this origins to config later
origins = [
    "http://localhost",
    "http://localhost:5173",
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(posts.router)
app.include_router(auth_router)


def main():
    uvicorn.run(
        "arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True
    )
