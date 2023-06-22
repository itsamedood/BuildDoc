from enum import Enum


class VariableType(Enum):
    REGULAR     = 0
    ENVIRONMENT = 1


class VariableScope(Enum):
    GLOBAL = 0
    LOCAL  = 1


class Variable: ...
