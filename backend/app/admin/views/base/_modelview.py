from typing import Any
from fastapi import Request
from sqladmin.models import ModelView

from ._query import CustomQuery


class CustomModelView(ModelView):
    
    async def delete_model(self, request: Request, pk: Any) -> None:
        await CustomQuery(self).delete(pk, request)

    async def insert_model(self, request: Request, data: dict) -> Any:
        return await CustomQuery(self).insert(data, request)

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        return await CustomQuery(self).update(pk, data, request)