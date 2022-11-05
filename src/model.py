from typing import Any, Dict


class Model:

    def __init__(self, **kwargs: Any):
        self._kwargs: Dict[Any, Any] = kwargs
    
    @property
    def get_values(self) -> Dict[Any, Any]:
        return self._kwargs
    