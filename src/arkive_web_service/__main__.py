from typing import Union
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
import uvicorn
import requests
from jose import jwt
from dotenv import dotenv_values
from fastapi.responses import RedirectResponse
import secrets

config = dotenv_values(".env")
app = FastAPI()
oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="http://localhost:8000", tokenUrl="token")

GOOGLE_CLIENT_ID = config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = config["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = config["GOOGLE_REDIRECT_URI"]


# ------ SESSION -----
# TODO: move this to dedicated session storage


# TODO: add sessions here
# TODO: move login calls to separate helpers
# TODO: add other SSOs

@app.get("/login/google", response_class=RedirectResponse)
async def login_google():
    return RedirectResponse(url=f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline")


@app.get("/auth/google")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token", None)
    if access_token is None:
        return "Error!"
    user_info = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}") #, headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()


@app.get("/token")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])


def main():
    uvicorn.run("arkive_web_service.__main__:app", host="0.0.0.0", port=8000, reload=True)
