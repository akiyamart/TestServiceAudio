
from typing import Annotated


from fastapi import HTTPException, Depends, status
from fastapi.security import SecurityScopes
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from .oauth import CookieAuthorization
from ..db import get_db
from ..profile import get_profile
from ...config.settings import settings
from ...utils.logger import logger
from ...schemas import TokenData, AdminSchema

cookie_oauth2_scheme = CookieAuthorization()

async def authentification_process(
    tokens: TokenData,
    security_scopes: SecurityScopes,
    session: AsyncSession | None = None,
):
    authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Incorrect authorization value",
        headers={"WWW-Authenticate": authenticate_value},
    )
    access_token = tokens.access_token
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    try:
        payload = jwt.decode(
            access_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        sub: str | None = payload.get("sub")
        await logger.write(f'An attempt to access a private resource. Checking the token for rights')
        if sub is None:
            raise  
        token_scopes: list = payload.get("scopes", [])
    except JWTError or ValidationError or ExpiredSignatureError:
        raise credentials_exception
    if not(set(token_scopes).issubset(set(security_scopes.scopes))):
        await logger.write(
            f'Profile have not enough permissions for executing this request. Access is denied'
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
    profile = await get_profile(filter_=sub, role=security_scopes.scopes[0], session=session)
    if not profile:
        raise credentials_exception
    return profile


async def authentificate_user(
    tokens: Annotated[TokenData, Depends(cookie_oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    user: dict = await authentification_process(tokens=tokens, security_scopes=SecurityScopes(scopes=["user", "admin"]), session=session)
    await logger.write(f"The user {user['login']} passed the checking")
    return user

async def authentificate_admin(
    tokens: TokenData,
    session: Annotated[AsyncSession, Depends(get_db)],
) -> AdminSchema:
    admin: dict = await authentification_process(tokens=tokens, security_scopes=SecurityScopes(scopes=["admin"]), session=session)
    await logger.write(f"The admin {admin['login']} passed the checking")
    return admin
