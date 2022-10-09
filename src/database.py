from collections import deque
from ctypes import Union
from lib2to3.pgen2.token import OP
import logging
from os import PathLike
from re import L
from sqlite3 import Connection, Cursor, connect
from typing import Any, Deque, Dict, List, Optional, TypeAlias
import typing


logger = logging.getLogger("OSqlite")

# stable


class Database():

    def __init__(self, database: str | bytes | PathLike[str] | PathLike[bytes],
                 **kwargs
                 ):
        """
        init database

        Args:
            database (StrOrBytesPath)
            kwargs (dict)
        """
        self._database: str | bytes | PathLike[str] | PathLike[bytes] = database
        self._command: deque = deque()
        self.__kwargs: Dict = kwargs
        self._connection: Connection
        self._cursor: Cursor
        self._tables: Dict[str, object] = {}

        self._value: tuple = ()
        self._cache_command: dict[str, Any] = {
            '_name': '',
            '_handle': '',
            '_keys': [],
        }

    def connect(self):
        """
        对数据库进行链接
        """
        self._connection = connect(self._database, **self.__kwargs)
        self._cursor = self._connection.cursor()
        return self

    def log(self, message: str):
        """
        log 相关
        """
        logger.info(message)

    def close(self):
        """
        对数据库进行一次提交后关闭
        """
        self.log("正在储存并关闭数据库")
        self._connection.commit()
        self._connection.close()

    def unsafe_close(self):
        """
        关闭数据库，但不保存
        """
        self._connection.close()

    def save(self):
        """
        储存数据库
        """
        self.log("正在储存数据库")
        self._connection.commit()
        return self

    def rollback(self):
        """
        回退上次操作
        """
        self._connection.rollback()
        return self

    def build(self):
        """
        构建 SQL 语句
        """
        self._cursor = self._connection.cursor()
        __c: dict[str, Any] = self._cache_command
        match (__c['_handle']):
            case 'create_table':
                self._command.appendleft(
                    f"CREATE TABLE IF NOT EXISTS {__c['_name']}({','.join(__c['_keys'])});")
            case 'delete_table':
                self._command.appendleft(f"DROP TABLE {__c['name']}")
        return self

    def show(self):
        """
        返回上一次构建的 SQL 语句

        Returns:
            str: SQL 语句
        """
        __c = self._command.pop()
        self._command.append(__c)
        return __c

    def request(self):
        """
        将命令构建并传输给数据库
        """
        self.build()
        self._cursor.execute(self._command.pop(), *self._value)
        return self

    def create_table(self, name: str):
        """
        新建一个表

        Args:
            name (str): 表的名字
        """
        self._cache_command["_name"] = name
        self._cache_command["_handle"] = 'create_table'
        return self

    def key(self, name: str, type: str = 'TEXT', other: Optional[str] = None):
        """
        构建在表中的键

        Args:
            name (str): 键的名字
            type (str): 键的类型. 默认为 TEXT.
            other (str): 额外的约束. 默认为 None. 
        """
        not_null = ''
        if type.startswith("NULL_"):
            type = type.lstrip("NULL_")
            not_null = "NOT NULL"
        self._cache_command["_keys"].append(
            f'{name} {type} {other} {not_null}')
        return self

    def delete_table(self, name: str):
        """
        删除一个表

        Args:
            name (str): 表的名字
        """
        self._cache_command["_name"] = name
        self._cache_command["_handle"] = 'delete_table'

    def table(self, cls):
        """
        表的解析与添加
        """
        def getattr(name):
            try:
                return cls.__getattribute__(name)
            except:
                return None

        anno = cls.__annotations__
        for i in cls.__annotations__:
            self.key(i, self.get_sql_type(anno[i]), getattr(i))
        self.create_table(cls.__name__).build().request()

        return cls

    def get_sql_type(self, name) -> str:
        """
        将对象里的类型注释转换为字符串

        Args:
            name (typing): 需转换的类型

        Returns:
            str: 转换后的字符串
        """
        types = {str: "TEXT",
                 int: "INT",
                 float: "REAL",
                 bytes: "BLOB",
                 Optional[str]: "TEXT",
                 Optional[int]: "INT",
                 Optional[float]: "REAL",
                 Optional[bytes]: "BLOB", }
        return types[name]

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        self.close()

    # def type_handler(self, cls):
    #     if (isinstance(cls, str)):
    #         return DataType.TEXT
        # if


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


class Model:
    _values = {}

    def __init__(self, *args, **kwargs):
        self._kwargs: dict = kwargs
        self._args: tuple = args

    def __setattr__(self, __name: str, __value: Any):
        self._values[__name] = __value
