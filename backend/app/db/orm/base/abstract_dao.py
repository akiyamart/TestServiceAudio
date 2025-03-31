from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

class AbstractDataAccessObject(ABC):
    
    def __init__(
        self, 
        db_session: AsyncSession
    ) -> None:
        self._db_session = db_session
    
    @abstractmethod
    async def fetch_model():
        raise NotImplementedError()
    
    @abstractmethod
    async def fetch_models():
        raise NotImplementedError()
    
    @abstractmethod
    async def create_model():
        raise NotImplementedError()
    
    @abstractmethod
    async def insert_models():
        raise NotImplementedError()
    
    @abstractmethod
    async def update_models():
        raise NotImplementedError()
    
    @abstractmethod
    async def update_model():
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_model():
        raise NotImplementedError()