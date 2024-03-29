from fastapi import APIRouter, Request
from ...utils import get_user_from_database_using_id

router = APIRouter(tags=["profile", "user"])


@router.get("/users/me")
async def read_users_me(request: Request):
    return await get_user_from_database_using_id(request.state.user_id)
