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

from src.database import Database, Model, Setting
from typing import Optional

db = Database("dwda.sqlite").connect()

@db.table
class Test(Model):
    omg: str = Setting(default="sdhawta")
    test: Optional[int]

db.close()

#or 

# a = Test(omg='dadadada.sqlite')
# print(dir(a), a._kwargs)
# a.omg="g"
# with db as s:
# s.add(a)
#     s.select(Test).where()
