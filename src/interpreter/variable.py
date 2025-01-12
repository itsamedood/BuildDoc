from enum import Enum


class VariableType(Enum):
  REGULAR     = 0
  ENVIRONMENT = 1
  SHELL       = 2  # I forgot what this was for...


# class VariableScope(Enum):
#   GLOBAL = 0
#   LOCAL  = 1


class Variable:
  """ Represents a variable, declared in the script or in a `.env`. """

  def __init__(self, _name: str, _value: str | int | float | bool, _type: VariableType) -> None:
    self.name, self.value, self.type = _name, _value, _type
