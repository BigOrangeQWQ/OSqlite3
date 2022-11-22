from typing import Any


class Setting:
    
    def __init__(self,primary_key: bool = False,
            unique: bool = False,
            not_null: bool = False,
            default: Any = None,
            check: str = '') -> None:
        """
            Args:
                primary_key (bool): 是否为主键. 默认为 False.
                not_null (bool): 是否不为空. 默认为 False.
                unique (bool): 是否允许储存键里两个相同的值. 默认为 False
                default (Any) 设置表中默认的值.
                check (str) 为表中的值增加约束条件.
        """
        self.primary_key: bool = primary_key
        self.unique: bool = unique
        self.default: Any = default 
        self.check: str = check
        self.not_null: bool = not_null
    
    def __repr__(self) -> str:

        return 'PRIMARY KEY ' if self.primary_key else '' + \
        'NOT_NULL ' if self.not_null else '' + \
        'UNIQUE ' if self.unique else '' + \
        f'DEFAULT {self.default} ' if self.default != None else '' + self.check

