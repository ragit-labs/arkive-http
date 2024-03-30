from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import login_required
import uvicorn

from .endpoints import posts
from .endpoints import auth
from .endpoints import profile
from .endpoints import processor

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

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(profile.router, dependencies=[Depends(login_required)])
app.include_router(processor.router)


def main():
    uvicorn.run(
        "arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True
    )
