from datetime import timedelta

import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from arkive_db.models import User
from arkive_web_service.enums import SignInProvider

from ..constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..utils.auth import create_access_token
from ..utils.user import get_user_from_database, insert_user_to_database


class TokenRequest(BaseModel):
    google_access_token: str


router = APIRouter(tags=["login", "google", "sso"])


class Token(BaseModel):
    access_token: str
    token_type: str


async def authenticate_user(google_access_token: str) -> User:
    response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={google_access_token}"
    )
    user_info = response.json()
    if "email" not in user_info:
        raise Exception("Something went wrong. Could not find user email in response.")
    email = user_info["email"]
    user = await get_user_from_database(email)
    if user is None:
        user = await insert_user_to_database(
            email,
            user_info.get("name"),
            user_info.get("given_name"),
            SignInProvider.GOOGLE,
            user_info.get("family_name", None),
            user_info.get("picture", None),
        )
    user = await get_user_from_database(email)
    if user is None:
        raise Exception("Something went wrong. Could not find user in database.")
    return user


@router.post("/authenticate/google", response_model=Token)
async def login_for_access_token(token_request: TokenRequest) -> JSONResponse:
    user = await authenticate_user(token_request.google_access_token)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or passwor. No user found."
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": str(user.id)}, expires_delta=access_token_expires
    )
    return JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "Bearer",
            "expiry": ACCESS_TOKEN_EXPIRE_MINUTES,
        },
        status_code=200,
    )
