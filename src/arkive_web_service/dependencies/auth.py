from typing import Optional

from fastapi import HTTPException, Request
from jose import jwt

from ..constants import JWT_ALGORITHM, JWT_SECRET_KEY
from ..utils.auth import parse_user_id_from_token
import logging
logger = logging.getLogger(__name__)


async def _get_token(request: Request) -> str:
    authorization: Optional[str] = request.headers.get("Authorization")
    print("==========Authorization: %s", authorization)
    if authorization is None:
        raise HTTPException(status_code=400, detail="Authorization header is not set.")
    token = None
    if authorization:
        try:
            scheme, _, param = authorization.partition(" ")
            if scheme.lower() == "bearer":
                token = param
            else:
                raise HTTPException(status_code=422, detail="Invalid token format")
        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail=f"Something went wrong while parsing the authorization token: {ex}",
            )
    else:
        raise HTTPException(status_code=400, detail="Authorization header is not set.")

    return token


async def login_required(request: Request) -> None:
    token = await _get_token(request)
    user_id = await parse_user_id_from_token(token)
    if user_id is None:
        raise HTTPException(status_code=422, detail="Unable to get user id from token")
    request.state.user_id = user_id


async def admin_only(request: Request) -> None:
    token = await _get_token(request)
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    if "admin" not in payload or not payload["admin"]:
        raise HTTPException(status_code=403, detail="Unauthorized access")
