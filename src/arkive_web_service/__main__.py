from typing import Union
from fastapi import FastAPI
import uvicorn


app = FastAPI()

@app.get("/")
def root():
    return "Hello, world! Welcome to Arkive!"


def main():
    uvicorn.run("arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True)
