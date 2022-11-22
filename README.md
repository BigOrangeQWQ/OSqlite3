# OrangeSqlite3
对 Sqlite3 库本身进行了一个简单的封装  
以更好的方便的调用Sqlite  
如有使用需求请搜索SqlModel  

## 安装 OrangeSqlite3

本人发现自己对数据库的认知和使用还是过于浅薄  
以及实现太过于不优雅和非常屎山  
因此此库的确是个人拿来学习并个人使用的  
所以有需要者请直接下载源码自行使用  


## 如何创建表与数据库
```py
db = Database("test.sqlite")

@db.table

class Test(Model):
    omg: str = Setting(default="default")
    test: Optional[int]

a=Test(omg='test',test=1)

with db.connect() as s:
    s.add(a)
```

## 选择一些元素
```py
with db.connect() as s:
    s.select
```