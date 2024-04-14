from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import select
from arkive_db.models import Note, NoteBlock

from ...database import db
from ...dependencies.auth import login_required
from ...settings import settings

router = APIRouter(tags=["bookmarks", "feed"])


class SaveRequestData(BaseModel):
    title: Optional[str] = Field(None, title="Title of the note")
    session_id: Optional[str] = Field(None, title="Session ID")
    url: Optional[str] = Field(None, title="URL of the website to be saved")
    content: Optional[str] = Field(None, title="Content of the note")
    blocks: Optional[list] = Field(None, title="Blocks of the note")
    folder_id: Optional[str] = Field(None, title="Folder ID")
    extra_metadata: Optional[dict] = Field(None, title="Extra metadata")
    note_type: Optional[str] = Field(None, title="Note type")


class NotesRequest(BaseModel):
    folder_id: Optional[str] = Field(None, title="Folder ID")


@router.post("/v2/notes/save", dependencies=[Depends(login_required)])
async def save_note(request: Request, data: SaveRequestData) -> JSONResponse:
    try:
        async with db.session() as session:
            note_blocks = [
                NoteBlock(
                    content=block["content"],
                    block_type=block["block_type"],
                ) for block in data.blocks
            ]
            note = Note(
                title=data.title,
                session_id=data.session_id,
                url=data.url,
                content=data.content,
                blocks=note_blocks,
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


@router.post("/v2/notes/get", dependencies=[Depends(login_required)])
async def get_notes(request: Request, data: NotesRequest) -> JSONResponse:
    try:
        async with db.session() as session:
            query = select(Note).filter(Note.user_id == request.state.user_id).filter(Note.folder_id == data.folder_id)
            result = (await session.execute(query)).scalars().all()
            notes = [
                {
                    "id": str(note.id),
                    "title": note.title,
                    "session_id": note.session_id,
                    "url": note.url,
                    "content": note.content,
                    "blocks": [
                        {
                            "id": str(block.id),
                            "content": block.content,
                            "block_type": block.block_type,
                        } for block in note.blocks
                    ],
                    "folder_id": str(note.folder_id),
                    "timestamp": str(note.timestamp),
                } for note in result
            ]
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while fetching notes: {ex}",
        )
    return JSONResponse(content=notes, status_code=200)
