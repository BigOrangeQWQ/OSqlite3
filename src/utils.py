from typing import Any


def Setting(primary_key: bool = False,
            unique: bool = False,
            not_null: bool = False,
            default: Any = None,
            check: str = '') -> Any:
    """
        Args:
            primary_key (bool): 是否为主键. 默认为 False.
            not_null (bool): 是否不为空. 默认为 False.
            unique (bool): 是否允许储存键里两个相同的值. 默认为 False
            default (Any) 设置表中默认的值.
            check (str) 为表中的值增加约束条件.
    """
    return 'PRIMARY KEY ' if primary_key else '' + \
        'NOT_NULL ' if not_null else '' + \
        'UNIQUE ' if unique else '' + \
        f'DEFAULT {default} ' if default != None else '' + check

