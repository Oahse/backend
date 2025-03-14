import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
import aiohttp
from oauth2 import OAuth2ClientConfig, create_access_token
from models import User, Token

router = APIRouter()

# OAuth2 Configuration (for Google)
oauth2_config = OAuth2ClientConfig(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    authorization_url="https://accounts.google.com/o/oauth2/v2/auth",
    token_url="https://oauth2.googleapis.com/token"
)

# Endpoint to start the OAuth2 flow (redirect to Google OAuth2 login)
@router.get("/login/google")
async def login_google():
    authorization_url = f"{oauth2_config.authorization_url}?response_type=code&client_id={oauth2_config.client_id}&redirect_uri={oauth2_config.redirect_uri}&scope=openid%20email"
    return RedirectResponse(authorization_url)

# OAuth2 Callback handler to exchange the code for the token
@router.get("/auth/google/callback")
async def auth_google_callback(code: str):
    # Exchange the code for a token
    async with aiohttp.ClientSession() as session:
        data = {
            "code": code,
            "client_id": oauth2_config.client_id,
            "client_secret": oauth2_config.client_secret,
            "redirect_uri": oauth2_config.redirect_uri,
            "grant_type": "authorization_code",
        }
        async with session.post(oauth2_config.token_url, data=data) as response:
            token_data = await response.json()
            access_token = token_data.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not get access token")
            
            # Get user data using the access token
            async with session.get("https://www.googleapis.com/oauth2/v1/userinfo?alt=json", headers={"Authorization": f"Bearer {access_token}"}) as user_response:
                user_info = await user_response.json()
                user = User(
                    id=user_info['id'],
                    username=user_info['name'],
                    email=user_info['email'],
                    role="user"  # Example role
                )
                # Create and return a JWT token
                token = create_access_token(data={"sub": user.id})
                return Token(access_token=token, token_type="bearer")
