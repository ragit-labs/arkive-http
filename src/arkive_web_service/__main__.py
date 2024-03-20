from fastapi import FastAPI
import uvicorn

from .endpoints import login


app = FastAPI()
app.include_router(login.router)


def main():
    uvicorn.run(
        "arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True
    )
