from fastapi import Request, Response, HTTPException
from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..dependencies.auth import AuthorizationService
from ..utils.cache import Cache
from ..config.settings import settings

class RefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        if request.cookies.get("access_token") and request.cookies.get("refresh_token"):
            if response.status_code == 401:
                try:
                    new_access_token = AuthorizationService.refresh_token(refresh_token=request.cookies.get("refresh_token"))
                    response.set_cookie("access_token", new_access_token, httponly=True, secure=True, samesite="none")
                except HTTPException as e:
                    return ORJSONResponse(
                        status_code=e.status_code,
                        content={"detail": e.detail}
                    )
        return response