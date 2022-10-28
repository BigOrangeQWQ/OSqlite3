from typing import Any, Dict

class Model:

    def __init__(self, **kwargs):
        self._kwargs: dict = kwargs
    
    @property
    def _get_values(self):
        return self._kwargs
    