import openai
from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
import json
from datetime import datetime
from fastapi.responses import JSONResponse
from ...dependencies import login_required
from ...types import PostInsertRequestData
from ..posts.utils import insert_post_for_user


client = openai.OpenAI(api_key="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")

SYSTEM = "Summarize this scraped website data. If there are authors, give author name else do not give it. Return response in only JSON format and nothing else. In JSON keep two keys, summary and author. Author can be null."

router = APIRouter(tags=["bookmarks", "feed"])


class SaveRequestData(BaseModel):
    url: str
    raw_data: str


@router.post("/save", dependencies=[Depends(login_required)])
async def save_url(request: Request, data: SaveRequestData) -> JSONResponse:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": data.raw_data},
            ],
        )
        response_parsed = json.loads(response.choices[0].message.content)
        title = response_parsed["title"]
        summary = response_parsed["summary"]
        author = response_parsed["author"]
        post_data = PostInsertRequestData(
            title=title,
            content=summary,
            url=data.url,
            banner="https://fastly.picsum.photos/id/790/200/300.jpg?hmac=FVbUQYv_h5C4v5_RAIja_q1c5UShyHhRu6C7DvjZM8U",
            timestamp=datetime.utcnow(),
            tags=["Test", "Startup"],
            extra_metadata={"author": author},
            user_id=request.state.user_id,
        )
        await insert_post_for_user(post_data)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while saving the url: {ex}",
        )
    return JSONResponse(content={"success": True}, status_code=201)
