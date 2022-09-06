# OrangeSqlite3
对 Sqlite3 库本身进行了一个简单的链式封装
以更好的方便的使用sqlite数据库

## 创建表
```py
db = Database("test_sqlite").connect()
db.create_table("test_table").key("ID", primary_key=True).key("name").request()
```
