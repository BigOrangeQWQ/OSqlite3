# OrangeSqlite3
对 Sqlite3 库本身进行了一个简单的封装  
以更好的方便的调用sqlite  
如有使用需求请搜索SqlModel  

## 安装 OrangeSqlite3

本人发现自己对数据库的认知和使用还是过于浅薄  
以及实现太过于不优雅和非常屎山  
因此此库的确是个人拿来学习并个人使用的  
所以有需要者请直接下载源码自行使用  

## 创建表
```py
from src.database import Database, Model, Setting
from typing import Optional

db = Database("test.sqlite").connect()

@db.table
class Test(Model):
    omg: str = Setting(default="default")
    test: Optional[int]

db.close()
```
## 鸽子计划
· 支持更多的语句  
· 对Setting入参的支持  
· 支持上下文操作  
· 覆写Model  
· 支持写入数据库  
