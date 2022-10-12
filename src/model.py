from typing import Any, Dict


class Model:
    _values = {'args': tuple(),
               'logic': Dict[Any, str],}

    def __init__(self, *args, **kwargs):
#         self.kwargs: dict = kwargs  
        _values.update(kwargs)
        _values['args'] = args
#         self.args: tuple = args

#     def __setattr__(self, __name: str, __value: Any):
#         self._values[__name] = __value
        
    def __eq__(self, __o: Any):
        self._values['logic'][__o] == f' == __o'
