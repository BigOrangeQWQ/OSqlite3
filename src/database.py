from collections import deque
import logging
from os import PathLike
from sqlite3 import Connection, Cursor, connect
from typing import Dict, List, TypeAlias
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
        self.deque = deque()
        self._cache_command = {
            '_name': str,
            '_handle': str,
            '_key': list,
        }

    def connect(self):
        """
        try to connnect database
        """
        self.connection = connect(self.database, **self.kwargs)
        return self

    def logger(self, message: str):
        """
        database logging
        """
        logger.info(message)

    def close(self):
        """
        commit and close database
        """
        self.logger("正在储存并关闭数据库")
        self.connection.commit()
        self.connection.close()

    def unsafe_close(self):
        """
        close database , but not commit.
        """
        self.connection.close()

    def save(self) -> Self:
        """
        commit database
        """
        self.logger("正在储存数据库")
        self.connection.commit()
        return self

    def rollback(self) -> Self:
        """
        rollback last handle
        """
        self.connection.rollback()
        return self

    def create_table(self, name: str) -> Self:
        """create a table

        Args:
            name (str): table name
        """
        self._cache_command["_name"] = name
        self._cache_command["_handle"] = 'create_table' 
        return self

    def key(self, name: str, type: str = 'TEXT', primary_key: bool = False, not_null: bool = False) -> Self:
        _key = 'PRIMARY KEY' if (primary_key) else ''
        _key = _key + ' NOT NULL' if (not_null) else _key
        self._cache_command["_keys"].append(f'{name} {type} {_key}')
        return self

    def show(self):
        pass

# testgit remote add origin git@github.com:BigOrangeQWQ/OSqlite3.git
