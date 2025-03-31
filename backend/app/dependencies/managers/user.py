from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from .base.manager import ManagerAbstractBase
from ...utils.logger import logger
from ...repositories import UserRepository
from ...schemas import (
    UserSchema,
    UserInsertSchema,
    UserUpdate,
    CaseInfo
)

class UserManager(ManagerAbstractBase):
    def __init__(
        self,
        db_session: AsyncSession
    ) -> None:
        self._db_session = db_session
        self.dao = UserRepository[UserSchema](db_session=db_session)
    
    async def fetch_model(
        self, 
        **filters
    ) -> dict:
        await logger.write(f"Fetching user with filter {filters}")
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
        await logger.write(f"Fetching users with filter {filters}")
        if response := await self.dao.fetch_models(
            order_by=order_by,
            offset=offset,
            limit=25,
            **filters
        ):
            return [obj.model_dump() for obj in response]
    
    async def create_model_from_schema(self, schema: UserInsertSchema) -> str:
        return await super().create_model_from_schema(schema)

    async def update_model_from_schema(
        self, 
        id: str,
        schema: UserUpdate,
        returning: str | None = None
    ) -> None | Any:
        data = self._formatting_data(schema=schema)
        result = await self.dao.update_model(
            data=data,
            id__eq=id,
            returning=returning,
        )
        return result
    
    async def update_models(
        self,
        cases: tuple[str, list[CaseInfo]],
        **filters
    ):
        await self.dao.update_models(
            cases=cases,
            **filters
        )

    async def delete_model(
        self, 
        id: str
    ) -> None:
        await self.dao.delete_model(id__eq=id)