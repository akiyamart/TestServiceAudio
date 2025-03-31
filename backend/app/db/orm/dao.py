from typing import Any, TypeVar

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import NoResultFound

from .base.abstract_dao import AbstractDataAccessObject
from .query import SelectQueryConstructor
from .filter import create_filter
from .case import create_case
from .value import create_values
from ..models.base import Model
from ...schemas import CaseInfo
from ...utils.logger import logger

T = TypeVar("T")

class DataAccessObject[T](AbstractDataAccessObject):
    model: Model = None
    
    async def fetch_model(
        self,
        **filters
    ) -> T:
        stmt = select(self.model).filter(*create_filter(self.model, **filters))
        if result := (await self._db_session.execute(stmt)).scalar_one():
            return result.to_pydantic()

    
    async def fetch_models(
        self,
        joins: list[tuple[Model, tuple[Model, str] | None]] | None = None,
        order_by: str | None = None,
        desc: bool | None = None,
        offset: int = 0,
        limit: int = 25,
        **filters
    ) -> list[T] | None:
        base_stmt = (
            select(self.model)
            .filter(*create_filter(self.model, **filters))
            .offset(offset)
        )
        if limit:
            base_stmt = base_stmt.limit(limit)
        
        stmt = (
            SelectQueryConstructor(base_stmt, self.model)
            .join(joins)
            .order_by(order_by, desc)  
        )
        objs: list[Model] = (await self._db_session.execute(stmt.get_query())).unique().scalars().all()
        if objs:
            return [obj.to_pydantic() for obj in objs]
        

    async def create_model(
        self,
        data: dict,
        returning: str = "id",
    ): 
        obj: Model = self.model(**data)
        self._db_session.add(obj)
        await self._db_session.flush()
        instrumental = getattr(obj, returning)
        await logger.write(f"Model {self.model.__name__} successfully created")
        return instrumental
    
    async def sum_(
        self,
        sum_attr: str,
        **filters
    ) -> float:
        if instrumental := getattr(self.model, sum_attr):
            stmt = (
                select(func.sum(instrumental))
                .filter(*create_filter(self.model, **filters))
            )
            return (await self._db_session.execute(stmt)).scalar_one()
    
    async def count(
        self,
        **filters
    ) -> int:
        stmt = (
            select(func.count()).select_from(self.model)
            .filter(*create_filter(self.model, **filters))
        )
        return (await self._db_session.execute(stmt)).scalar_one()
    
    async def insert_models(
        self,
        data: list[dict]
    ):
        stmt = (
            insert(self.model)
            .values(data)
        )
        await self._db_session.execute(stmt)
        await self._db_session.flush()
        
        await logger.write(f"Models {self.model.__name__} successfully inserted")
        

    async def update_models(
        self,
        cases: tuple[str, list[CaseInfo]],
        **filters
    ):
        stmt = (
            update(self.model)
            .filter(*create_filter(self.model, **filters))
            .values(
                **create_case(self.model, cases)
            )
        )
        
        await self._db_session.execute(stmt)
        await self._db_session.flush()
        
        await logger.write(f"Models {self.model.__name__} successfully updated")
        
    
    async def update_model(
        self,
        data: dict[str, Any],
        returning: str = None,
        **filters
    ):
        stmt = (
            update(self.model)
            .filter(*create_filter(self.model, **filters))
            .values(**create_values(self.model, data))
        )
        if returning:
            if instrumental := getattr(self.model, returning):
                stmt = stmt.returning(instrumental)
        res = await self._db_session.execute(stmt)
        await self._db_session.flush()
        
        await logger.write(f"Model {self.model.__name__} successfully updated")
        
        if returning:
            try:
                return res.scalar_one_or_none()
            except:
                raise NoResultFound()
    
    async def delete_model(
        self,
        returning: str = None,
        **filters
    ):
        stmt = (
            delete(self.model)
            .filter(*create_filter(self.model, **filters))
        )
        if returning:
            if instrumental := getattr(self.model, returning):
                stmt = stmt.returning(instrumental)
        
        res = await self._db_session.execute(stmt)
        await self._db_session.flush()
        
        await logger.write(f"Model {self.model.__name__} successfully deleted")
        
        if returning:
            try:
                return res.scalar_one_or_none()
            except:
                raise NoResultFound()