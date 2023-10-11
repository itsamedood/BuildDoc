from enum import Enum


class VariableType(Enum):
    REGULAR     = 0
    ENVIRONMENT = 1


# class VariableScope(Enum):
#     GLOBAL = 0
#     LOCAL  = 1


class Variable:
    def __init__(self, _name: str, _value: str | int | float | bool, _type: VariableType) -> None:
        self.name, self.value, self.type = _name, _value, _type
