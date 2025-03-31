from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logger import logger
from app.api import (
    users_router,
    auth_router,
    audio_router
)
from app.utils.redis import redis_connection
from app.middlewares import RefreshMiddleware
from app.admin.setup import setup_admin


@asynccontextmanager
async def lifespan(_):
    await logger.write("The API service started")
    api.state.redis = await redis_connection.get_redis_connection()
    yield 
    await logger.write("The API service has shut down")
    await api.state.redis.close()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None, 
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_admin(app)

api = FastAPI(root_path="/api/v1")

api.add_middleware(RefreshMiddleware)

api.include_router(auth_router)
api.include_router(users_router)
api.include_router(audio_router)

app.mount("/api/v1", api)