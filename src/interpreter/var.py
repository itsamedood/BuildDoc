from enum import Enum
from typing import Any


class VarType(Enum):
  LOCAL = 0
  ENV   = 1


class Var:
  def __init__(self, name: str, value: Any, vtype: VarType) -> None:
    self.name, self.value, self.vtype = name, value, vtype
