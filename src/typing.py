class DataType():
    
    def __init__(self) -> None:
        self.NULL #NULL
        self.INTERGER #int
        self.TEXT #text
        self.BLOB #data
        self.REAL #float
    
    def __getattribute__(self, __name: str) -> str:
        return __name
    