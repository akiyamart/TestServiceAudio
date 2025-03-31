from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..config.settings import settings

engine = create_async_engine(url=settings.DATABASE_DSN, echo=False, pool_size=settings.DATABASE_POOL_SIZE)

async_session = async_sessionmaker(engine, expire_on_commit=True)
