from collections import deque
from os import PathLike
from sqlite3 import Connection, Cursor, connect
from typing import Any, Deque, Dict, List, Optional, Type, Union
from logging import getLogger
from typing_extensions import Self

from .model import Model


logger = getLogger("OSqlite")


class DatabaseBoolStr:
    def __init__(self, string: str):
        self.string = string

    def __and__(self, __o: object) -> str:
        return f"{self.string} AND {__o}"

    def __or__(self, __o: object) -> str:
        return f"{self.string} OR {__o}"

    def __repr__(self) -> str:
        return self.string
    
    
class DataBaseKey:

    def __init__(self, name: str, type: str = 'TEXT', other: str = '') -> None:
        self.name = name
        self.type = type
        self.other = other
        self._not = ''
        
    def __repr__(self) -> str:
        return f'{self.name} {self.type} {self.other}'

    def __eq__(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} == {__o}')

    def __lt__(self, __o: object) -> DatabaseBoolStr:
        if self._not == 'NOT':
            DatabaseBoolStr(f'{self.name} !< {__o}')
        return DatabaseBoolStr(f'{self.name} < {__o}')

    def __le__(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} <= {__o}')

    def __ne__(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} != {__o}')

    def __gt__(self, __o: object) -> DatabaseBoolStr:
        if self._not == 'NOT':
            DatabaseBoolStr(f'{self.name} !> {__o}')
        return DatabaseBoolStr(f'{self.name} > {__o}')

    def __ge__(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} >= {__o}')

    def __not__(self):
        self._not = 'NOT'
        
    def __contains__(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} {self._not} IN {__o}')
    
    def _glob(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} GLOB {__o}')
    
    def _like(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} LIKE {__o}')

    def _is_null(self) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} IS {self._not} NULL')
    
    def _exists(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} EXISTS {__o}')
    
    def _is(self, __o: object) -> DatabaseBoolStr:
        return DatabaseBoolStr(f'{self.name} IS {self._not} {__o}')
    
class CommandBuilder:

    def __init__(self, cls):
        """
        A SQL Command Builder

        Args:
            name (str, object): table 
        """
        self._class = cls
        self._name: str = cls.__class__.__name__ if cls.__class__.__name__ != 'type' else cls.__name__  # type: ignore
        self._command: str
        self._value: list[Any] = []
        self._handle: str
        self._keys: list[DataBaseKey] = []
        self._cache: Dict[str, Any] = {}
        self._where_statement: str | None = None

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
        self._keys.append(DataBaseKey(name, type, other))
        return self

    def delete_table(self) -> Self:
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

    def select(self, *keys: Any) -> Self:
        self._handle = 'select'
        self._value = list(keys)
        return self

    def where(self, statement: str | None):
        self._where = statement

    @property
    def build(self) -> List[Any]:
        """
        构建 SQL 语句
        """
        # python 3.10
        __r: str = ''
        match (self._handle):
            case 'create_table':
                __r = f"CREATE TABLE IF NOT EXISTS {self._name}({','.join([str(i) for i in self._keys])});"
            case 'delete_table':
                __r = f"DROP TABLE {self._name};"
            case 'insert':
                __r = f"INSERT INTO {self._name} ({','.join([i for i in self._cache])}) " + \
                    f"VALUES ({','.join(['?' for i in self._cache])});"  # type: ignore
                self._value = [self._cache.get(
                    i, None) for i in self._cache]
            case 'select':
                __r = f"SELECT {','.join(self._value)} FROM {self._name};"
            case _:
                ...

        if self._where_statement:
            __r += self._where_statement
        return [__r, self._value]


class DataBase(CommandBuilder):

    def __init__(self, database: Union[str, bytes, PathLike[str], PathLike[bytes]],
                 **kwargs: Any
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
        for i in list(self._command):  # type: ignore
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

    def commit(self) -> Self:
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

    def get(self) -> List[Any]:
        """
        return last build SQL command

        Returns:
            str: SQL command
        """
        __c: List[Any] = self._command.pop()
        self._command.append(__c)
        return __c

    def pop(self) -> List[Any]:
        """
        delete and get last build SQL command
        """
        return self._command.pop()

    def request(self) -> Self:
        """
        build SQL command and request database
        """
        __command = self._command.pop()
        self._cursor = self._connection.cursor()

        if __command[0].startwish("SELECT"):
            self._cursor.execute(__command[0])
            # keys = __command[1]
            # {i for i in __command[1]: v for v in result}
        else:
            self._cursor.execute(__command[0], __command[1])
        return self

    def table(self, cls: Any):
        """
        init tables
        """
        _anno: Dict[str, Any] = cls.__annotations__
        cmd: CommandBuilder = CommandBuilder(cls)
        for i in _anno:
            cmd.key(i, self.get_type(_anno[i]), getattr(cls, i, ''))
            setattr(cls, i, DataBaseKey(
                i, self.get_type(_anno[i]), getattr(cls, i, '')))
        self.append(cmd.create_table().build)
        return cls

    def add(self, cls: Model) -> Self:
        """
        add values to tables
        """
        cmd = CommandBuilder(cls).insert({i: cls.get_values.get(i)
                                          for i in cls.get_values})
        self.append(cmd.build).request()
        return self

    def select(self, cls: object):
        # cmd = CommandBuilder(cls).select()
        return CommandBuilder(cls).select()

    def get_type(self, name: Type[Any]) -> str:
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
        return types.get(name, "TEXT")  # type:ignore

    def append(self, command: List[Any]) -> Self:
        self._command.appendleft(command)
        return self

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args: Any):
        self.close()
