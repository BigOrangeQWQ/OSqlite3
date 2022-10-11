from collections import deque
import logging
from os import PathLike
from sqlite3 import Connection, Cursor, connect
from typing import Any, Deque, Dict, Optional

from .model import Model


logger = logging.getLogger("OSqlite")


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
        self._command: Deque = deque()
        self.__kwargs: Dict = kwargs
        self._connection: Connection
        self._cursor: Cursor
        self._tables: Dict[str, object] = {}

        self._value: tuple | list = []
        self._cache_command: Dict[str, Any] = {
            '_name': '',
            '_handle': '',
            '_keys': [],
            '_cache': {},
        }

    def connect(self):
        """
        对数据库进行链接
        """
        self._connection = connect(self._database, **self.__kwargs)
        self._cursor = self._connection.cursor()
        return self

    def close(self):
        """
        对数据库进行一次提交后关闭
        """
        logger.info("正在储存并关闭数据库")
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
        logger.info("正在储存数据库")
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
        __r = ''
        match (__c['_handle']):
            case 'create_table':
                __r = f"CREATE TABLE IF NOT EXISTS {__c['_name']}({','.join(__c['_keys'])});"
            case 'delete_table':
                __r = f"DROP TABLE {__c['_name']}"
            case 'insert':
                __r = f"INSERT INTO {__c['_name']} ({','.join([i for i in __c['_cache']])}) " + \
                        f"VALUES ({','.join(['?' for i in __c['_cache']])});"
                self._value = [__c["_cache"].get(i,None) for i in __c["_cache"]]
    
                
        self._command.appendleft(__r)
        logger.debug(__r)
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
        __command = self._command.pop()
        print(__command, self._value)
        self._cursor.execute(__command, tuple(self._value))
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

    def key(self, name: str, type: str = 'TEXT', other: str = ''):
        """
        构建在表中的键

        Args:
            name (str): 键的名字
            type (str): 键的类型. 默认为 TEXT.
            other (str): 额外的约束. 默认为 None. 
        """
        self._cache_command["_keys"].append(
            f'{name} {type} {other}')
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
                return cls.__dict__[name]
            except:
                return ''

        _anno = cls.__annotations__
        for i in _anno:
            self.key(i, self.get_type(_anno[i]), getattr(i))
            print(getattr(i))
        self.create_table(cls.__name__).request()  # type: ignore
        return cls
    
    def add(self, cls):
        """
        表的值的添加
        """
        self._cache_command['_cache'] = {i: cls._values['_kwargs'].get(i,None) for i in cls.__annotations__}
        self._cache_command['_handle'] = 'insert'
        self._cache_command['_name'] = cls.__class__.__name__
        self.request()
        return self

    def get_type(self, name) -> str:
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
                Optional[bytes]: "BLOB"}
        return types[name]

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        self.close()

