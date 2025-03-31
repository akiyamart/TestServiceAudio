import httpx
from fastapi import Depends, Request, status, HTTPException
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.routing import APIRouter

from ..config.settings import settings
from ..utils.logger import logger
from ..dependencies.db import get_db
from ..schemas import (
    LoginResponse, 
    UserInsertSchema
)
from ..dependencies.auth.authorization import AuthorizationService
from ..dependencies.administrator import Administrator

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.get( 
    "/login", 
)
async def login(request: Request): 
    await logger.write(
        f"{request.method} Request from {request.client.host}: {request.client.port} Handler /auth/login"
    )
    return {
        "url": f"https://oauth.yandex.ru/authorize?response_type=code&client_id={settings.YANDEX_CLIENT_ID}&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    }


@auth_router.get(
    "/yandex/callback",
    responses={
        200: {"model": LoginResponse}
    }
)
async def yandex_callaback(
    code: str,
    request: Request,
    db_session: AsyncSession = Depends(get_db),
):
    try:
        await logger.write(
            f"{request.method} Request from {request.client.host}: {request.client.port} Handler /auth/callback"
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth.yandex.ru/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": settings.YANDEX_CLIENT_ID,
                    "client_secret": settings.YANDEX_CLIENT_SECRET,
                    "redirect_uri": settings.YANDEX_REDIRECT_URI,
                },
            )  
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to auth in Yandex")
        
        yandex_token = response.json().get("access_token")
        if not yandex_token:
            raise HTTPException(status_code=400, detail="Access token cannot bu Nullable type")
        
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                "https://login.yandex.ru/info",
                headers={"Authorization": f"OAuth {yandex_token}"},
            )
        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user data")
        user_data = user_response.json()
        yandex_id: int = user_data.get("id")
        login: str = user_data.get("login")
        email: str = user_data.get("default_email")

        connector = Administrator(db_session)
        async with connector.start() as administrator: 
            user_list: list[dict] = await administrator.users.fetch_models(yandex_id__eq=yandex_id)

            if not user_list: 
                user_id: str = await administrator.users.create_model_from_schema(
                    UserInsertSchema(
                        yandex_id=yandex_id, 
                        login=login,
                        email=email
                    )
                )
            else:
                user_id = user_list[0]['user_id']

        if token_data := await AuthorizationService.login(user_id, role="user"):
            response = ORJSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "OK"}
            )
            response.set_cookie("access_token", token_data.access_token, httponly=True, secure=True, samesite="none")
            response.set_cookie("refresh_token", token_data.refresh_token, httponly=True, secure=True, samesite="none")
            return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The process can't be executed: {e}")
