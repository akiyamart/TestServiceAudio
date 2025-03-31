from typing import Any
from sqladmin._queries import Query
from sqlalchemy.ext.asyncio import AsyncSession

from sqladmin.helpers import (
    get_direction,
    is_falsy_value,
)


class CustomQuery(Query):
    
    async def _set_attributes_async(self, session: AsyncSession, obj: Any, data: dict) -> Any:
        for key, value in data.items():
            column = self.model_view._mapper.columns.get(key)
            relation = self.model_view._mapper.relationships.get(key)

            # Set falsy values to None, if column is Nullable
            if not value:
                if is_falsy_value(value) and not relation and column.nullable:
                    value = None
                setattr(obj, key, value)
                continue

            if relation:
                direction = get_direction(relation)
                if direction in ["ONETOMANY", "MANYTOMANY"]:
                    related_stmt = self._get_to_many_stmt(relation, value)
                    result = await session.execute(related_stmt)
                    related_objs = result.scalars().unique().all()
                    setattr(obj, key, related_objs)
                elif direction == "ONETOONE":
                    related_stmt = self._get_to_one_stmt(relation, value)
                    result = await session.execute(related_stmt)
                    related_obj = result.scalars().first()
                    setattr(obj, key, related_obj)
                else:
                    obj = self._set_many_to_one(obj, relation, value)
            else:
                setattr(obj, key, value)
        return obj