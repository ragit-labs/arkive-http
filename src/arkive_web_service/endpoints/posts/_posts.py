from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from .utils import get_all_cards_for_user, create_post
from arkive_web_service.mappers import post_to_json
from ...utils import get_user_from_database_using_id

router = APIRouter(tags=["bookmarks", "feed"])


@router.get("/all")
async def get_all(request: Request) -> JSONResponse:
    user = await get_user_from_database_using_id(request.state.user_id)
    posts = await get_all_cards_for_user(user.id)
    return JSONResponse(content=[post_to_json(post) for post in posts])
