from functools import wraps
from fastapi import HTTPException, Request, status
from datetime import datetime, timedelta
from ..constants import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_DEFAULT_EXPIRY
from jose import JWTError, jwt

from arkive_db.models import User
from arkive_web_service.database import db
from sqlalchemy import select
from arkive_web_service.enums import SignInProvider
from typing import Optional
from arkive_web_service.mappers import signin_provide_enum_to_database


async def get_user_from_database(email: str):
    async with db.session() as session:
        query = select(User).where(User.email == email)
        user = (await session.execute(query)).scalars().one_or_none()
        return user


async def get_user_from_database_using_id(id: str):
    async with db.session() as session:
        query = select(User).where(User.id == id)
        user = (await session.execute(query)).scalars().one_or_none()
        return user


async def insert_user_to_database(
    email: str,
    full_name: str,
    first_name: str,
    signin_provider: SignInProvider,
    last_name: Optional[str],
    display_picture_url: Optional[str],
):
    user = User(
        email=email,
        full_name=full_name,
        first_name=first_name,
        signin_provider=signin_provide_enum_to_database(signin_provider),
        last_name=last_name,
        display_picture_url=display_picture_url,
    )

    async with db.session() as session:
        session.add(user)
        try:
            await session.commit()
        except Exception as ex:
            raise Exception("Something went wrong while inserting the user", str(ex))
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_DEFAULT_EXPIRY)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def parse_user_id_from_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id
