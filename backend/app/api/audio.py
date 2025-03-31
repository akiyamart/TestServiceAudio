import shutil
from uuid import uuid4
from typing import Annotated, List
from pathlib import Path as PathLib

from fastapi import Depends, Request, status, HTTPException, File, UploadFile
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.auth import authentificate_user
from ..dependencies.administrator import Administrator
from ..utils.logger import logger
from ..dependencies.db import get_db
from ..schemas import (
    AudioSchema,
    AudioDefaultResponse,
    AudioInsertSchema,
    UserSchema
)

audio_router = APIRouter(prefix="/audio", tags=["Audio"])

@audio_router.get(
    "/all",
    responses={
        200: {"model": List[AudioSchema]}
    }
)
async def get_files(
    request: Request,
    user: Annotated[UserSchema, Depends(authentificate_user)],  
    db_session: AsyncSession = Depends(get_db),
):
    await logger.write(
        f"{request.method} Request from {request.client.host}:{request.client.port} Handler {user['user_id']} /audio/all"
    )    
    connector = Administrator(db_session)
    async with connector.start() as administrator:
        user_files = await administrator.audio.fetch_models(user_id__eq=user["user_id"])
        if user_files is None: 
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Not found user files"
            )
        return ORJSONResponse(
            status_code=status.HTTP_200_OK, 
            content={"files": user_files}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Can't process the request"
    )

@audio_router.post(
    "/upload", 
    responses={
        201: {"model": AudioDefaultResponse}
    }
)
async def upload_audio(
    request: Request,
    user: Annotated[UserSchema, Depends(authentificate_user)],  
    file: UploadFile = File(...),
    db_session: AsyncSession = Depends(get_db),
):  
    await logger.write(
        f"{request.method} Request from {request.client.host}:{request.client.port} Handler {user['user_id']} /audio/upload"
    )    
    connector = Administrator(db_session)
    async with connector.start() as administrator:
        file_id = f'{uuid4()}'
        filename = f"{file_id}_{file.filename}"
        
        upload_dir = PathLib("app/uploads")
        file_path = upload_dir / filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        await administrator.audio.create_model_from_schema(
            AudioInsertSchema(
                id=file_id,
                user_id=user['user_id'],
                name=filename,
                path=str(file_path)
            )
        )
        return ORJSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content={"status": "OK"}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Can't process the request"
    )