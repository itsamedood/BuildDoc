from enum import Enum
from typing import Any


class VariableType(Enum):
    REGULAR     = 0
    ENVIRONMENT = 1


# class VariableScope(Enum):
#     GLOBAL = 0
#     LOCAL  = 1


class Variable:
    def __init__(self, _name: str, _value: Any, _type: VariableType) -> None:
        self.name, self.value, self.type = _name, _value, _type
