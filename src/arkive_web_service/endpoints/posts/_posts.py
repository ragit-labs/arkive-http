from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from .utils import get_all_cards_for_user, get_post, is_valid_uuid
from ...utils import get_user_from_database_using_id
from ...dependencies import login_required

router = APIRouter(tags=["bookmarks", "feed"])


@router.get("/all", dependencies=[Depends(login_required)])
async def get_all(request: Request) -> JSONResponse:
    user = await get_user_from_database_using_id(request.state.user_id)
    posts = await get_all_cards_for_user(user.id)
    return posts


@router.get("/get/{post_id}")
async def get(request: Request, post_id: str):
    if not is_valid_uuid(post_id):
        raise HTTPException(status_code=422, detail="Invalid post id")
    post = await get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Not found")
    return post
