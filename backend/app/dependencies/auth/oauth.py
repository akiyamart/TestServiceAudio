from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2

from ...schemas.auth import TokenData

class CookieAuthorization(OAuth2):
    
    async def __call__(self, request: Request) -> str | None:
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        if ((not access_token) or (not refresh_token)):
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
                )
            else:
                return None
        return TokenData(access_token=access_token, refresh_token=refresh_token)