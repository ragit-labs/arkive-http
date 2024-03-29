from fastapi import Request, HTTPException
from ..utils import parse_user_id_from_token


async def _get_token(request: Request) -> str:
    authorization: str = request.headers.get("Authorization")
    token = None
    if authorization:
        try:
            scheme, _, param = authorization.partition(" ")
            if scheme.lower() == "bearer":
                token = param
            else:
                raise HTTPException("Invalid token format")
        except Exception as ex:
            raise HTTPException(
                "Something went wrong while parsing the authorization token", ex
            )
    else:
        raise HTTPException(status_code=400, detail="Authorization header is not set.")

    return token


async def login_required(request: Request) -> None:
    token = await _get_token(request)
    user_id = await parse_user_id_from_token(token)
    if user_id is None:
        raise HTTPException("Unable to get user id from token")
    request.state.user_id = user_id
