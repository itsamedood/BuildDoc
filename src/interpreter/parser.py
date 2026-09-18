from enum import Enum
from interpreter.token import Token  # Sleepy?
from typing import Any


class ReadingType:
  NONE                = 0  # Or maybe make this default to reading a task command?
  VARIABLE_NAME       = 1
  VARIABLE_VALUE      = 2
  TASK_NAME           = 3
  TASK_CMD            = 4
  SHELL_CMD           = 5


class Parser:
  """ Parses the tokens from the lexer. This is the messy part. """

  line, character = 0, 0
  variables: list[tuple[str, Any]]
  reading = 0

  def __init__(self) -> None: ...

  def parse_line(self) -> None: ...
