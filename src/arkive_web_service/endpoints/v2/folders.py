from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import select

from arkive_db.models import Folder

from ...database import db
from ...dependencies.auth import login_required
from ...settings import settings

router = APIRouter(tags=["folders"])


class CreateFolderRequestData(BaseModel):
    name: Optional[str] = Field(None, title="Name of the folder")


@router.post("/v2/folders/create", dependencies=[Depends(login_required)])
async def create_folder(request: Request, data: CreateFolderRequestData) -> JSONResponse:
    try:
        async with db.session() as session:
            query = select(Folder).filter(Folder.name == data.name and Folder.user_id == request.state.user_id)
            result = (await session.execute(query)).scalar_one_or_none()
            if result:
                raise HTTPException(
                    status_code=400,
                    detail="Folder with the same name already exists",
                )
            new_folder = Folder(
                name=data.name,
                user_id=request.state.user_id,
            )
            session.add(new_folder)
            await session.commit()
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while saving the note: {ex}",
        )
    return JSONResponse(content={"id": new_folder.id}, status_code=201)


@router.post("/v2/folders/get", dependencies=[Depends(login_required)])
async def get_folders(request: Request) -> JSONResponse:
    try:
        async with db.session() as session:
            query = select(Folder).filter(Folder.user_id == request.state.user_id)
            result = (await session.execute(query)).scalars().all()
            folders = [{"id": str(folder.id), "name": folder.name} for folder in result]
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong while fetching folders: {ex}",
        )
    return JSONResponse(content=folders, status_code=200)
