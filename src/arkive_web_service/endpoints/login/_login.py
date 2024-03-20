from fastapi import Depends, Request, APIRouter
from fastapi.security import OAuth2AuthorizationCodeBearer
import requests
from jose import jwt
from fastapi.responses import RedirectResponse
from arkive_web_service.settings import settings
from .utils import get_user_from_database, insert_user_to_database
from arkive_web_service.enums import SignInProvider


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://localhost:8000", tokenUrl="token"
)

router = APIRouter(tags=["login", "google", "sso"])


@router.get("/login/google", response_class=RedirectResponse)
async def login_google(request: Request):
    # TODO: move this url to constants
    return RedirectResponse(
        url=f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    )


@router.get("/auth/google")
async def auth_google(request: Request, code: str):

    # TODO: move this url to constants

    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token", None)
    if access_token is None:
        return "Error!"

    # TODO: move this url to constants
    response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
    )
    user_info = response.json()

    if "email" not in user_info:
        raise Exception("Something went wrong. Could not find user email in response.")

    email = user_info["email"]

    user = await get_user_from_database(email)

    if user is None:
        # Create new user in database
        insert_user_to_database(
            email,
            user.get("name"),
            user.get("given_name"),
            SignInProvider.GOOGLE,
            user.get("family_name", None),
            user.get("picture", None),
        )

    return user_info


@router.get("/token")
async def get_token(request: Request, token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, settings.GOOGLE_CLIENT_SECRET, algorithms=["HS256"])
