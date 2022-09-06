from collections import deque
import logging
from os import PathLike
from sqlite3 import Connection, Cursor, connect
from typing import Any, Deque, Dict, List, TypeAlias
from typing_extensions import Self

from .typing import DataType

logger = logging.getLogger("OSqlite")

# stable
StrOrBytesPath: TypeAlias = str | bytes | PathLike[str] | PathLike[bytes]


class Database():

    def __init__(self,
                 database: StrOrBytesPath,
                 **kwargs
                 ):
        """
        init database

        Args:
            database (StrOrBytesPath)
            kwargs (dict)
        """
        self.database: StrOrBytesPath = database
        self.kwargs: dict = kwargs
        self.connection: Connection
        self.cursor: Cursor
        self.tables: List[str] = []
        self.deque: Deque = deque()
        self._command: str = ''
        self._value: tuple = ()
        self._cache_command: dict[str, Any] = {
            '_name': str,
            '_handle': str,
            '_key': list,
        }

    def connect(self):
        """
        对数据库进行链接
        """
        self.connection = connect(self.database, **self.kwargs)
        return self

    def logger(self, message: str):
        """
        log 相关
        """
        logger.info(message)

    def close(self):
        """
        对数据库进行一次提交后关闭
        """
        self.logger("正在储存并关闭数据库")
        self.connection.commit()
        self.connection.close()

    def unsafe_close(self):
        """
        关闭数据库，但不保存
        """
        self.connection.close()

    def save(self) -> Self:
        """
        储存数据库
        """
        self.logger("正在储存数据库")
        self.connection.commit()
        return self

    def rollback(self) -> Self:
        """
        回退上次操作
        """
        self.connection.rollback()
        return self

    def build(self):
        """
        构建 SQL 语句
        """
        __c: dict[str, Any] = self._cache_command
        match (__c['_handle']):
            case 'create_table':
                self._command = f"CREATE TABLE {__c['name']}({','.join(__c['_keys'])});"
                return self

    def show(self):
        """
        返回上一次构建的 SQL 语句

        Returns:
            str: SQL 语句
        """
        return self._command

    def request(self):
        """
        将命令构建并传输给数据库
        """
        self.build()
        self.cursor.execute(self._command, self._value)

    def create_table(self, name: str) -> Self:
        """
        新建一个表

        Args:
            name (str): 表的名字
        """
        self._cache_command["_name"] = name
        self._cache_command["_handle"] = 'create_table'
        return self

    def key(self, name: str, type: str = 'TEXT', primary_key: bool = False, unique: bool = False,
            not_null: bool = False, default: str = '') -> Self:
        """
        构建在表中的键

        Args:
            name (str): 键的名字
            type (str, DataType): 键的类型. 默认为 TEXT.
            primary_key (bool): 是否为主键. 默认为 False.
            not_null (bool): 是否不为空. 默认为 False.
            unique (bool): 是否允许储存键里两个相同的值. 默认为 False
            default (str) 设置表中默认的值
        """
        # _key = 'PRIMARY KEY' if (primary_key) else ''
        # _key = _key + ' NOT NULL' if (not_null) else _key
        _key = ''
        self._cache_command["_keys"].append(f'{name} {type} {_key}')
        return self
    