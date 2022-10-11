from typing import Any


class Model:
    _values = {}

    def __init__(self, *args, **kwargs):
        self._kwargs: dict = kwargs
        self._args: tuple = args

    def __setattr__(self, __name: str, __value: Any):
        self._values[__name] = __value
