from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from ..dependencies.auth import admin_only, login_required
from ..post_filter_engine.types import GetAllRequest
from ..types import PostDeleteRequestData, PostInsertRequestData, PostUpdateRequestData
from ..utils.post import (
    get_all_posts_for_user_conditioned,
    get_post,
    insert_post_for_user,
    is_valid_uuid,
    remove_post_for_user,
    update_post_for_user,
)

router = APIRouter(tags=["bookmarks", "feed"])


@router.post("/all", dependencies=[Depends(login_required)])
async def get_all_where(
    request: Request, get_all_request: GetAllRequest
) -> JSONResponse:
    return await get_all_posts_for_user_conditioned(
        request.state.user_id, get_all_request
    )  # type: ignore


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


@router.post("/update", dependencies=[Depends(login_required)])
async def update_post(request: Request, data: PostUpdateRequestData) -> JSONResponse:
    user_id = request.state.user_id
    try:
        await update_post_for_user(user_id, data.post_id, data.title, data.content)
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wront while inserting the post: {ex}",
        )
    return JSONResponse(content={"success": True}, status_code=201)
