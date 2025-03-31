from typing import TypeVar

from ..db.models import AudioOrm
from ..db.orm.dao import DataAccessObject

T = TypeVar("T")

class AudioRepository(DataAccessObject[T]):
    model = AudioOrm
    