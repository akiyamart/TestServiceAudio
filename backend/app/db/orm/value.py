from typing import Any

from ..models import Model
    
def create_values(
    model: Model,
    data: dict[str, Any],
) -> dict[str, Any]:
    fields = {}
    for field, value in data.items():
        target_value = value
        if isinstance(target_value, dict):
            if delta := target_value.get("delta"):
                target_value = getattr(model, field) + delta
            elif delta == 0:
                continue
        fields.update( 
            {
                field: target_value
            }
        )
    return fields