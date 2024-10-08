import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..dependencies.auth import login_required
from ..settings import settings
from ..utils.decorators import fire_and_forget

router = APIRouter(tags=["bookmarks", "feed"])


class SaveRequestData(BaseModel):
    url: str = Field(..., title="URL of the website to be saved")
    raw_data: str = Field(..., title="Raw data of the website")


@fire_and_forget
def send_to_processor(data: dict):
    url = f"{settings.ARKIVE_LLM_API_URI}/handle"
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
