# class test():
    
#     def __init__(self) -> None:
#         self.test = "OMG"
        
#     def __eq__(self, __o: object) -> bool:
#         # print(__o.__class__.__dict__)
#         print(__o)
#         return True
    
#     def condition(self):
#         return self

    
# print(test().condition() == "dawda")

# from typing import Any, Optional

# def Setting(default: Optional[str]) -> Any:
#     return "dsdadadas"
    

# class test:
#     odaw: Optional[int] = Setting(default='dawdawd')
#     dowu: str
     
    
# print(test().__getattribute__('odaw'))

# from src.database import Database, Model, Setting
# from typing import Optional

# from mimetypes import init
# from typing import Any, Optional
# from src.database import DataBase
# from src.model import Model
# from src.utils import Setting



# b = Test(doing=3)
# a = Test(omg='dwada',doing=1)
# print(a,b)
# with db.connect() as s:
#     s.add(a)
#     s.add(b)

# a = Test(doing=3)
# # print(a._values)
# # print(dir(Test))
# # # print(dir(a), a._kwargs)  
# # a.omg="g"
# db.add(a)
# db.close()
# print(Test.__dict__)
# print(Test.__getattribute__(Test,'omg'))
# print(Test.__dict__['omg'])
#     s.select(Test).where()

# from src.model import Model


# class Test(Model):
#     omg: str
#     adawdaw: str

# g= ["d", 'f']
# def a(b, c):
#     print(b,"   ",c)
    
# a(*g)

# import inspect

# # print(('d' == 'h').__class__.__dict__)

# def out():
#     inspect.getsource()

# out()

# from src.model import Model
# from src.database import DataBase
# from src.utils import Setting

# #注册一个数据库
# db = DataBase("dwda.sqlite")

# @db.table
# class Test(Model):
#     omg: str
#     doing: int = Setting(default=1)
    
# with db as s:
#     s.select(Test,).where(Test.omg == "dwadawd")



# import requests
# from lxml import etree

# r = requests.get("https://ncov.dxy.cn/ncovh5/view/pneumonia")

# with open("test.html", "w",encoding='UTF-8') as f:
#     f.write(r.content.decode())  
# a  = etree.parse("test.html", etree.HTMLParser())
# d = (a.xpath("//script[@id='getAreaStat']/text()"))

# print(d)
