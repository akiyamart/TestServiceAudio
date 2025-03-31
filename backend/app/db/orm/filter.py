from sqlalchemy import func

from ..models import Model

class SqlAlchemyFilterUnit:
    
    def __init__(
        self,
        model: Model,
        attr: str,
        value: str
    ) -> None:
        self.model = model
        self.attr = attr
        self.value = value
      
    @property  
    def eq(
        self
    ):
        """Equal"""
        return getattr(self.model, self.attr) == self.value
       
    @property 
    def ge(
        self
    ):
        """Greater equal"""
        return getattr(self.model, self.attr) >= self.value
    
    @property
    def gt(
        self
    ):
        """Greater than"""
        return getattr(self.model, self.attr) > self.value
    
    @property
    def le(
        self
    ):
        """Less equal"""
        return getattr(self.model, self.attr) <= self.value
    
    @property
    def lt(
        self
    ):
        """Less than"""
        return getattr(self.model, self.attr) < self.value
    
    @property
    def ne(
        self
    ):
        """Not equal"""
        return getattr(self.model, self.attr) != self.value
    
    @property
    def in_(
        self
    ):
        """In iterable"""
        return getattr(self.model, self.attr).in_(self.value)
    
    @property
    def notin_(
        self
    ):
        """Not in iterable"""
        return getattr(self.model, self.attr).notin_(self.value)
    
    @property
    def match(self):
        """FTS filter"""
        instrumental = getattr(self.model, self.attr)
        ts_vector = func.to_tsvector("english", self.value)
        ts_query = (func.plainto_tsquery("english", instrumental))
        return ts_vector.op("@@")(ts_query)

def create_filter(
    model: Model,
    **kwargs
):  
    if kwargs:
        conditions = [
            getattr((SqlAlchemyFilterUnit(model, condition.split("__")[0], value)), condition.split("__")[1])
            for condition, value in kwargs.items() if value is not None
        ]
        return conditions
    return []