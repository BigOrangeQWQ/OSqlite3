# OrangeSqlite3
对 Sqlite3 库本身进行了一个简单的链式封装
以更好的方便的使用sqlite数据库

## 安装 OrangeSqlite3

本人发现自己对数据库的认知和使用还是过于浅薄
以及实现太过于不优雅和非常屎山
因此此库的确是个人拿来学习并个人使用的
所以有需要者请直接下载源码自行使用

## 创建表代码示例
```py
from OSqlite import Database
from OSqlite import DataType

db = Database("test_sqlite").connect()
db.create_table("test_table").key(name="ID", type= DataType.INT, primary_key=True) \
                             .key("name", DataType.TEXT).request()
```
