from typing import Any, Dict, List

from src.database import CommandKey


class Model:

    def __init__(self, **kwargs: Any):
        self._kwargs: Dict[Any, Any] = kwargs
    
    @property
    def get_values(self) -> Dict[Any, Any]:
        return self._kwargs
    
    
class Table:
    def __init__(self, name: str, key: List[CommandKey]) -> None:
        """
        Table data init

        Args:
            name (str): table name  
            key (List[CommandKey]): table keys
        """
        self.name = name
        self.key = key 
        
class Column(list):
    pass