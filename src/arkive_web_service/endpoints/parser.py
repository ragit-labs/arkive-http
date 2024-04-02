from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from ..dependencies.auth import login_required
from ..utils.decorators import fire_and_forget
import requests


router = APIRouter(tags=["bookmarks", "feed"])


class SaveRequestData(BaseModel):
    url: str = Field(..., title="URL of the website to be saved")
    raw_data: str = Field(..., title="Raw data of the website")


@fire_and_forget
def send_to_processor(data: dict):
    url = (
        "https://ea98-2405-201-300a-8bd9-8d3a-8ff1-6212-4d06.ngrok-free.app/handle/html"
    )
    response = requests.post(url, json=data)
    print(response.status_code)


@router.post("/save", dependencies=[Depends(login_required)])
async def save_url(request: Request, data: SaveRequestData) -> JSONResponse:
    try:
        send_to_processor(
            {"url": data.url, "html": data.raw_data, "user": request.state.user_id}
        )
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while saving the url: {ex}",
        )
    return JSONResponse(content={"success": True}, status_code=201)
