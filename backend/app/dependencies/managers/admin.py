from sqlalchemy.ext.asyncio import AsyncSession

from .base.manager import ManagerAbstractBase
from ...utils.logger import logger
from ...repositories import AdminRepository
from ...schemas import (
    AdminSchema,
)

class AdminManager(ManagerAbstractBase):
    def __init__(
        self,
        db_session: AsyncSession
    ) -> None:
        self._db_session = db_session
        self.dao = AdminRepository[AdminSchema](db_session=db_session)
    
    async def fetch_model(
        self, 
        **filters
    ) -> dict:
        await logger.write(f"Fetching audio with filter {filters}")
        if response := await self.dao.fetch_model(
            **filters
        ):
            return response.model_dump()
        
    async def fetch_models(
        self,
        order_by: str = None,
        offset: int = 0,
        **filters
    ) -> list[dict]:
        await logger.write(f"Fetching audios with filter {filters}")
        if response := await self.dao.fetch_models(
            order_by=order_by,
            offset=offset,
            limit=25,
            **filters
        ):
            return [obj.model_dump() for obj in response]
    