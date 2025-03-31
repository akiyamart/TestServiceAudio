from typing import TypeVar

from ..db.models import UserOrm
from ..db.orm.dao import DataAccessObject

T = TypeVar("T")

class UserRepository(DataAccessObject[T]):
    model = UserOrm
    