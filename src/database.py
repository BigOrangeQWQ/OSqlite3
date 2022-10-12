from collections import deque
from os import PathLike
from sqlite3 import Connection, Cursor, connect
from typing import Any, Deque, Dict, List, Optional, Union
from logging import getLogger


from .model import Model


logger = getLogger("OSqlite")


class CommandBuilder:
    
    def __init__(self, name: Union[str,object]):
        """
        A SQL Command Builder

        Args:
            name (str, object): table 
        """
        self._name = name if name is str else name.__class__.__name__
        self._command: str
        self._value: Union[list, tuple] = []
        self._handle: str
        self._keys: list = []
        self._cache: Dict[str, Any] = {}

    def create_table(self):
        """
        create this table
        """
        
        self._handle = 'create_table'
        return self

    def key(self, name: str, type: str = 'TEXT', other: str = ''):
        """
        构建在表中的键

        Args:
            name (str): 键的名字
            type (str): 键的类型. 默认为 TEXT.
            other (str): 额外的约束. 默认为 None. 
        """
        self._keys.append(
            f'{name} {type} {other}')
        return self

    def delete_table(self):
        """
        delete this table
        """
        self._handle = 'delete_table'
        return self

    def insert(self, values: Dict[str, Any]):
        """insert some data in tables

        Args:
            values (Dict[str, Any]): data
        """
        self._handle = 'insert'
        self._cache = values
        
    def select(self, ):
        pass
    
    def where(self):
        pass
    
    def build(self):
        """
        构建 SQL 语句
        """
        __r = ''
        match (self._handle):
            case 'create_table':
                __r = f"CREATE TABLE IF NOT EXISTS {self._name}({','.join(self._keys)});"
            case 'delete_table':
                __r = f"DROP TABLE {self._name}"
            case 'insert':
                __r = f"INSERT INTO {self._name} ({','.join([i for i in self._cache])}) " + \
                    f"VALUES ({','.join(['?' for i in self._cache])});"
                self._value = [self._cache.get(i, None) for i in self._cache]
        return __r


class DataBase():

    def __init__(self, database: Union[str, bytes, PathLike[str], PathLike[bytes]],
                **kwargs
                ):
        """
        init database

        Args:
            database (StrOrBytesPath)
            kwargs (dict)
        """
        self._database: Union[str, bytes,
                            PathLike[str], PathLike[bytes]] = database
        self._command: Deque[str] = deque()
        self._tables: Deque[str] = deque()
        self.__kwargs: Dict[Any, Any] = kwargs
        self._connection: Connection
        self._cursor: Cursor

    def connect(self):
        """
        connect sqlite
        """
        self._connection = connect(self._database, **self.__kwargs)
        self._build_tables()
        self._cursor = self._connection.cursor()
        return self

    def close(self):
        """
        commit data then close this database
        """
        logger.info(f"closing database")
        self._connection.commit()
        self._connection.close()

    def unsafe_close(self):
        """
        close this sqlite
        """
        self._connection.close()

    def save(self):
        """
        commit data to database
        """
        logger.debug("commiting data to database")
        self._connection.commit()
        return self

    def rollback(self):
        """
        rollback last request SQL command
        """
        self._connection.rollback()
        return self

    def get(self):
        """
        return last build SQL command

        Returns:
            str: SQL command
        """
        __c = self._command.pop()
        self._command.append(__c)
        return __c

    def pop(self):
        """
        获得上一次构建的 SQL 语句
        并将其从命令队列里删除
        """
        return self._command.pop()

    def request(self):
        """
        build SQL command and request database
        """
        
        # self._cursor = self._connection.cursor()
        # __command = self._command.pop()
        # self._cursor.execute(__command, tuple(self._value))
        # logger.debug(__command, self._value)
        # print(__command, self._value)
        # return self
    
    def table(self, cls):
        """
        init tables
        """
        def getattr(name):
            try:
                return cls.__dict__[name]
            except:
                return ''

        _anno = cls.__annotations__
        # for i in _anno:
        #     self.key(i, self.get_type(_anno[i]), getattr(i))
        # self.create_table(cls.__name__).build() 
        # self._tables.append(self.pop())
        return cls
    
    def _build_tables(self):
        """
        初始化表
        """
        # for i in list(self._tables):
            # self._reqcmd(self._tables.pop())

    def add(self, cls):
        """
        add values to tables
        """
        # {i: cls._values['_kwargs'].get(i,None) for i in cls.__annotations__}
        CommandBuilder(cls.__class__.__name__)
        # self._cache_command['_cache'] = {
        #     i: cls._values['_kwargs'].get(i) for i in cls._values['_kwargs']}
        # self._cache_command['_handle'] = 'insert'
        # self._cache_command['_name'] = cls.__class__.__name__
        self.request()
        return self

    def get_type(self, name) -> str:
        """
        Converts type comments in an object to strings

        Args:
            name (typing): comment type

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
