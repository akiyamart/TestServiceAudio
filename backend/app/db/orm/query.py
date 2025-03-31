import typing as tp

from sqlalchemy.sql import Select

from ..models import Model
    
class SelectQueryConstructor:
    
    def __init__(
        self,
        stmt: tp.Optional[Select[tp.Any]],
        model: Model
    ) -> None:
        self.stmt = stmt
        self.model = model
    
    def join(
        self, 
        joins: list[tuple[Model, tuple[Model, str] | None]] = None
    ) -> "SelectQueryConstructor":
        if isinstance(joins, list):
            for join in joins:
                target, target_info = join
                if target_info:
                    join_condition = (getattr(self.stmt.columns_clause_froms[0].c, target_info[0]) == getattr(target, target_info[1]))
                    self.stmt = self.stmt.join(target, *join_condition)
                else:
                    self.stmt = self.stmt.join(target)
        return self
    
    def order_by(
        self,
        attr: str = None,
        desc: bool = False
    ) -> "SelectQueryConstructor":
        if attr:
            if instrumental := getattr(self.model, attr):
                if desc:
                    instrumental = instrumental.desc()
                self.stmt = self.stmt.order_by(instrumental)
        return self
    
    def get_query(self) -> Select[tp.Any]:
        return self.stmt