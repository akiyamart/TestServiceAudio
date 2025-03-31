from sqlalchemy import case
from sqlalchemy.sql.elements import Case

from ..models import Model
from ...schemas import CaseInfo, ChangeOnDelta
    
def create_case(
    model: Model,
    cases_info: tuple[str, list[CaseInfo]]
) -> dict[str, Case]:
    attr, cases = cases_info
    whens = []
    for case_ in cases:
        update_value = case_.update_value
        if isinstance(update_value, ChangeOnDelta):
            update_value = getattr(model, attr) + update_value.delta
        whens.append(
            (
                getattr(model, case_.condition_field) == case_.condition_value, update_value
            )
        )
    return {
        attr: case(
            *whens
        )
    }