from typing import Annotated

from fastapi import Depends, Request, Path, status, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.auth import authentificate_user
from ..dependencies.administrator import Administrator
from ..utils.logger import logger
from ..dependencies.db import get_db
from ..schemas import (
    UserSchema,
    UserUpdate,
    UserDefaultResponse
)

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get(
    "/{id}",
    responses={
        200: {"model": UserSchema}
    }
)
async def get_user(
    request: Request,
    id: Annotated[str, Path()],
    db_session: AsyncSession = Depends(get_db),
): 
    await logger.write(
        f"{request.method} Request from {request.client.host}: {request.client.port} Handler /users/{id}"
    )
    connector = Administrator(db_session)
    async with connector.start() as administrator:
        user = await administrator.users.fetch_model(id__eq=id)
        return ORJSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"user": user}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Can`t procces the request"
    )

@users_router.patch(
    "", 
    responses={
        200: {"model": UserDefaultResponse}
    }
)
async def update_user(
    request: Request,
    user: Annotated[UserSchema, Depends(authentificate_user)],  
    body: UserUpdate,
    db_session: AsyncSession = Depends(get_db),
):  
    await logger.write(
        f"{request.method} Request from {request.client.host}: {request.client.port} Handler {user["user_id"]} /users/"
    )    
    connector = Administrator(db_session)
    async with connector.start() as administrator:
        await administrator.users.update_model_from_schema(
            id=user["user_id"], 
            schema=body
        )
        return ORJSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"status": "OK"}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Can`t procces the request"
    )

@users_router.delete(
    "/", 
    responses={
        200: {"model": UserDefaultResponse}
    }
)
async def delete_user(
    request: Request,
    user: Annotated[UserSchema, Depends(authentificate_user)],  
    db_session: AsyncSession = Depends(get_db),
):
    await logger.write(
        f"{request.method} Request from {request.client.host}: {request.client.port} Handler {user["user_id"]} /users/"
    )    
    connector = Administrator(db_session)
    async with connector.start() as administrator:
        await administrator.users.delete_model(id=user["user_id"])
        response = ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "OK"}
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Can`t procces the request"
    )