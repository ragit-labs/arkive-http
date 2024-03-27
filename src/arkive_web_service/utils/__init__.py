from functools import wraps
from fastapi import HTTPException, Request, status
from datetime import datetime, timedelta
from ..constants import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from typing import Callable
from ..endpoints.login.utils import get_user_from_database_using_id


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def parse_user_from_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = await get_user_from_database_using_id(user_id)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


async def get_current_user(request: Request):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing.")
    token = authorization.split("Bearer ")[1] if len(authorization.split(" ")) > 1 else None
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    user = await parse_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def login_required(endpoint: Callable):
    async def wrapper(*args, **kwargs):
        await get_current_user(*args, **kwargs)
        return await endpoint(*args, **kwargs)
    return wrapper
