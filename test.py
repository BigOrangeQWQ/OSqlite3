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

from mimetypes import init
from typing import Any, Optional
from src.database import Database
from src.model import Model
from src.utils import Setting


db = Database("dwda.sqlite").connect()

@db.table
class Test(Model):
    omg: str = Setting(default="sdhawta")
    doing: int


a = Test(omg='dadadada')
print(a._values)
# print(dir(Test))
# # print(dir(a), a._kwargs)
# a.omg="g"
db.add(a)
db.close()
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