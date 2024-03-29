from fastapi import APIRouter, Request
from pydantic import BaseModel
from ...utils.process_html import process_html


router = APIRouter(tags=["llm", "processor"])


class SaveResponse(BaseModel):
    success: bool


class SaveRequest(BaseModel):
    url: str
    raw_html: str


@router.post("/save", response_model=SaveResponse)
async def save(data: SaveRequest):
    content = await process_html(data.raw_html)
    print("-=------------", content)
    return {"success": True}
