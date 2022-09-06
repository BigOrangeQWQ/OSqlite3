# OrangeSqlite3
对 Sqlite3 库本身进行了一个简单的链式封装
以更好的方便的使用sqlite数据库

## 安装 OrangeSqlite3

```
pip install OSqlite3
```
## 创建表代码示例
```py
from OSqlite import Database
from OSqlite import DataType

db = Database("test_sqlite").connect()
db.create_table("test_table").key(name="ID", type= DataType.INT, primary_key=True)\
                             .key("name", DataType.TEXT).request()
```
