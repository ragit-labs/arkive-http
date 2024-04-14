from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime

from arkive_db.models import Note

from ...database import db
from ...dependencies.auth import login_required
from ...settings import settings

router = APIRouter(tags=["bookmarks", "feed"])


class SaveRequestData(BaseModel):
    title: Optional[str] = Field(None, title="Title of the note")
    session_id: Optional[str] = Field(None, title="Session ID")
    url: Optional[str] = Field(None, title="URL of the website to be saved")
    content: Optional[str] = Field(None, title="Content of the note")
    note: Optional[str] = Field(None, title="Note")
    folder_id: Optional[str] = Field(None, title="Folder ID")
    extra_metadata: Optional[dict] = Field(None, title="Extra metadata")
    note_type: Optional[str] = Field(None, title="Note type")


@router.post("/v2/save/note", dependencies=[Depends(login_required)])
async def save_url(request: Request, data: SaveRequestData) -> JSONResponse:
    try:
        async with db.session() as session:
            note = Note(
                title=data.title,
                session_id=data.session_id,
                url=data.url,
                content=data.content,
                note=data.note,
                folder_id=data.folder_id,
                extra_metadata=data.extra_metadata,
                note_type=data.note_type,
                user_id=request.state.user_id,
                timestamp=datetime.utcnow(),
            )
            session.add(note)
            await session.commit()
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while saving the note: {ex}",
        )
    return JSONResponse(content={"success": True}, status_code=201)
