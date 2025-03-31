from contextlib import asynccontextmanager

from ..db.engine import async_session

@asynccontextmanager
async def get_db(): 
    async with async_session() as session: 
        yield session