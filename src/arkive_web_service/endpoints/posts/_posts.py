from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from .utils import (
    get_all_cards_for_user,
    get_post,
    is_valid_uuid,
    remove_post_for_user,
    insert_post_for_user,
)
from ...utils import get_user_from_database_using_id
from ...dependencies import login_required, admin_only
from ...types import PostDeleteRequestData, PostInsertRequestData


router = APIRouter(tags=["bookmarks", "feed"])


@router.get("/all", dependencies=[Depends(login_required)])
async def get_all(request: Request) -> JSONResponse:
    user = await get_user_from_database_using_id(request.state.user_id)
    posts = await get_all_cards_for_user(user.id)
    return posts  # type: ignore


@router.get("/get/{post_id}")
async def get(request: Request, post_id: str) -> JSONResponse:
    if not is_valid_uuid(post_id):
        raise HTTPException(status_code=422, detail="Invalid post id")
    post = await get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Not found")
    return post  # type: ignore


@router.post("/delete", dependencies=[Depends(login_required)])
async def delete_post(request: Request, data: PostDeleteRequestData) -> JSONResponse:
    post_id = data.post_id
    if not is_valid_uuid(post_id):
        raise HTTPException(status_code=422, detail="Invalid post id")
    try:
        await remove_post_for_user(post_id, request.state.user_id)
    except HTTPException as ex:
        raise ex
    except Exception as ex:
        raise HTTPException(status_code=503, detail=f"Something went wrong {ex}")
    return JSONResponse(content={"success": True}, status_code=200)


@router.post("/insert", dependencies=[Depends(admin_only)])
async def insert_post(request: Request, data: PostInsertRequestData) -> JSONResponse:
    try:
        await insert_post_for_user(data)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wront while inserting the post: {ex}",
        )
    return JSONResponse(content={"success": True}, status_code=201)
