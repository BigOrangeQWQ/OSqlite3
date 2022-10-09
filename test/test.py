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

from typing import Any, Optional

def Setting(default: Optional[str]) -> Any:
    return "dsdadadas"
    

class test:
    odaw: Optional[int] = Setting(default='dawdawd')
    dowu: str
     
    
print(test().__getattribute__('odaw'))