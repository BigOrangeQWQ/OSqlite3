from collections import deque
from os import PathLike
from sqlite3 import Connection, Cursor, connect
from typing import Any, Collection, Deque, Dict, List, Optional, Union
from logging import getLogger
from typing_extensions import Self

from .model import Model


logger = getLogger("OSqlite")


class CommandBuilder:

    def __init__(self, cls):
        """
        A SQL Command Builder

        Args:
            name (str, object): table 
        """
        self._class = cls
        # print(cls.__name__)
        self._name = cls.__class__.__name__ if cls.__class__.__name__ != 'type' else cls.__name__
        self._command: str
        self._value: List = []
        self._handle: str
        self._keys: list = []
        self._cache: Dict[str, Any] = {}

    def create_table(self) -> Self:
        """
        create this table
        """

        self._handle = 'create_table'
        return self

    def key(self, name: str, type: str = 'TEXT', other: str = '') -> Self:
        """
        构建在表中的键

        Args:
            name (str): name.
            type (str): type. default is TEXT.
            other (str): other setting. default is  None. 
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

    def insert(self, values: Dict[str, Any]) -> Self:
        """insert some data in tables

        Args:
            values (Dict[str, Any]): data
        """
        self._handle = 'insert'
        self._cache = values
        return self

    def select(self, ):
        pass

    def where(self):
        pass

    @property
    def build(self) -> List[str|list]:
        """
        构建 SQL 语句
        """
        # python 3.10
        __r = ''
        match (self._handle):
            case 'create_table':
                __r = f"CREATE TABLE IF NOT EXISTS {self._name}({','.join(self._keys)});"
            case 'delete_table':
                __r = f"DROP TABLE {self._name}"
            case 'insert':
                __r = f"INSERT INTO {self._name} ({','.join([i for i in self._cache])}) " + \
                    f"VALUES ({','.join(['?' for i in self._cache])});"
                self._value: List = [self._cache.get(i, None) for i in self._cache]
        return [__r, self._value]


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
        self._data = Dict 
        self._database: Union[str, bytes,
                            PathLike[str], PathLike[bytes]] = database
        self._command: Deque[List[Any]] = deque()
        self.__kwargs: Dict[Any, Any] = kwargs
        self._connection: Connection
        self._cursor: Cursor
        
    def connect(self) -> Self:
        """
        connect sqlite
        """
        self._connection = connect(self._database, **self.__kwargs)
        self._cursor = self._connection.cursor()
        for i in list(self._command):
            self.request()
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

    def save(self) -> Self:
        """
        commit data to database
        """
        logger.debug("commiting data to database")
        self._connection.commit()
        return self

    def rollback(self) -> Self:
        """
        rollback last request SQL command
        """
        self._connection.rollback()
        return self

    def get(self) -> List:
        """
        return last build SQL command

        Returns:
            str: SQL command
        """
        __c = self._command.pop()
        self._command.append(__c)
        return __c 

    def pop(self) -> List:
        """
        delete and get last build SQL command
        """
        return self._command.pop()

    def request(self) -> Self:
        """
        build SQL command and request database
        """
        __command = self._command.pop()
        # print(__command)
        self._cursor = self._connection.cursor()
        result = self._cursor.execute(__command[0], __command[1])
        return self

    def table(self, cls):
        """
        init tables
        """
        _anno = cls.__annotations__
        cmd = CommandBuilder(cls)
        def getattr(name):
            try:
                return cls.__dict__[name]
            except:
                return ''
            
        for i in _anno:
            cmd.key(i, self.get_type(_anno[i]), getattr(i))
        self.append(cmd.create_table().build)
        return cls

    def add(self, cls) -> Self:
        """
        add values to tables
        """
        cmd = CommandBuilder(cls).insert({i: cls._get_values.get(i)
                        for i in cls._get_values})
        self.append(cmd.build).request()
        return self

    def get_type(self, name) -> str:
        """
        Converts type comments in an object to strings

        Args:
            name (typing): comment type

        Returns: str
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

    def append(self, command) -> Self:
        self._command.appendleft(command)
        return self
    
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        self.close()
