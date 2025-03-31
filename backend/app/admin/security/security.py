from sqladmin.authentication import AuthenticationBackend

from fastapi import Request, HTTPException

from ..db import get_db
from ...dependencies.auth.authorization import AuthorizationService
from ...dependencies.auth.authentification import authentificate_admin
from ...schemas import TokenData

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        login, password = form["username"], form["password"]
        try:
            async with get_db() as session:
                token_data = await AuthorizationService.login(
                    data={"login": login, "password": password},
                    role='admin',
                    session=session
                )
                if token_data:
                    request.session.update(
                        {
                            'access_token': token_data.access_token,
                            'refresh_token': token_data.refresh_token
                        }
                    )
                    return True
        except Exception as e:
            print(f"Login error: {e}") 
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear() 
        return False

    async def authenticate(self, request: Request) -> bool:
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        if (access_token and refresh_token):
            if await authentication_process_admin(access_token, refresh_token, request):
                return True
        return False
    

async def authentication_process_admin(
    access_token: str, 
    refresh_token: str, 
    request: Request, 
) -> bool:
    tokens = TokenData(
        access_token=access_token, 
        refresh_token=refresh_token
    )

    async with get_db() as session:
        try:
            is_authenticated = await authentificate_admin(tokens=tokens, session=session)
            if is_authenticated:
                return True
        except HTTPException as e:
            if e.status_code == 401:
                pass
            else:
                return False
        try:
            refreshed_access_token: str = AuthorizationService.refresh_token(refresh_token=refresh_token)
            request.session.update({
                'access_token': refreshed_access_token,
                'refresh_token': refresh_token
            })
            new_tokens = TokenData(
                access_token=refreshed_access_token,
                refresh_token=refresh_token
            )
            is_authenticated = await authentificate_admin(tokens=new_tokens, session=session)
            if is_authenticated:
                return True
        except Exception as e:
            print(f"Failed to refresh tokens: {e}")

    return False

authentication_backend = AdminAuth(secret_key="85758aab4f5b11dd03fd7b2a8b3da25ef4e511da77354b5630a0ab95ec9bcf1c")