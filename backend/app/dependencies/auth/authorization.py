from typing import  Optional, Literal
from datetime import datetime, timedelta, UTC

from jose import jwt
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..administrator import Administrator
from ..hasher import Hasher
from ...config.settings import settings
from ...schemas import TokenData

class AuthorizationService: 
    
    @classmethod
    async def login(cls, data: str | dict, role: Literal["user", "admin"], session: AsyncSession = None) -> TokenData | None:
        if role == "admin":
            return await cls._procces_authorization_admin(data, session)
        elif role == "user": 
            return cls._procces_authorization_user(data)

    @classmethod    
    def _procces_authorization_user(cls, user_id: str) -> TokenData | None:
        try:
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            access_token = cls.create_access_token( 
                data={ 
                    "sub": user_id, 
                    "scopes": ["user"]
                },
                expires_delta=access_token_expires
            )
            refresh_token = cls.create_refresh_token(
                data={ 
                    "sub": user_id, 
                    "scopes": ["user"]
                },
                expires_delta=refresh_token_expires
            )
            return TokenData(
                access_token=access_token,
                refresh_token=refresh_token
            )
        except: 
            raise HTTPException( 
                status_code=status.HTTP_400_BAD_REQUEST, detail="The process can`t be executed"
            )
        
    @classmethod
    async def _procces_authorization_admin(cls, data: dict, session: AsyncSession): 
        connector = Administrator(session)
        async with connector.start() as administrator: 
            admin: dict = await administrator.admin.fetch_model(login__eq=data["login"])
            if Hasher.verify_password(data["password"], admin['password_hash']): 
                access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
                access_token = cls.create_access_token( 
                    data={ 
                        "sub": admin['login'], 
                        "scopes": ["admin"]
                    },
                    expires_delta=access_token_expires
                )
                refresh_token = cls.create_refresh_token(
                    data={ 
                        "sub": admin['login'], 
                        "scopes": ["admin"]
                    },
                    expires_delta=refresh_token_expires
                )
                return TokenData(
                    access_token=access_token,
                    refresh_token=refresh_token
                )

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @classmethod
    def refresh_token(cls, refresh_token: str):
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        new_access_token = cls.create_access_token(data={"sub": payload["sub"], "scopes": payload["scopes"]})

        return new_access_token