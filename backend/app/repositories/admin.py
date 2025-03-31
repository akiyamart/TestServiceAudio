from typing import TypeVar

from ..db.models import AdminOrm
from ..db.orm.dao import DataAccessObject

T = TypeVar("T")

class AdminRepository(DataAccessObject[T]):
    model = AdminOrm
    