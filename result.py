from enum import Enum

class ResultType(Enum):
    ERROR=0
    SUCCESS=1

    def __str__(self) -> str:
        return f'{self.name}'

class Result :
    def __init__(self, result_type: ResultType,  message: str):
        self.result_type = result_type
        self.message = message

    def __str__(self) -> str:
        return str('[' + str(self.result_type) + '] ' + self.message)