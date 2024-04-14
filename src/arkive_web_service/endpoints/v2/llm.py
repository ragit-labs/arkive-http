from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ...llm.summarizer import summarizer
from ...llm.explainer import explainer

from ...dependencies.auth import login_required

router = APIRouter(tags=["llm", "summary"])


class LLMTextData(BaseModel):
    submittedText: str = Field(..., title="Text submitted by the user")


@router.post("/v2/llm/summarize", dependencies=[Depends(login_required)])
async def save_note(request: Request, data: LLMTextData) -> JSONResponse:
    try:
        return JSONResponse(content={"data": summarizer(data.submittedText)}, status_code=200)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while summarizing the text: {ex}",
        )


@router.post("/v2/llm/explain", dependencies=[Depends(login_required)])
async def save_note(request: Request, data: LLMTextData) -> JSONResponse:
    try:
        return JSONResponse(content={"data": explainer(data.submittedText)}, status_code=200)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while explaining the text: {ex}",
        )
