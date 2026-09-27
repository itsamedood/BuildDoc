from enum import Enum
from interpreter.token import Token  # Sleepy?
from typing import Any


class ReadingType:
  TASK_CMD            = 0  # Default because it's going to be the most used. I think.
  VARIABLE_NAME       = 1
  VARIABLE_VALUE      = 2
  TASK_NAME           = 3
  SHELL_CMD           = 4


class Parser:
  """ Parses the tokens from the lexer. This is the messy part. """

  line, character = 0, 0
  current_task, task_name = '', ''
  varname, varvalue = '', ''
  variables: list[tuple[str, Any]]
  reading = -1  # None of them just in case so we don't fuck up and parse something as a task command.

  def __init__(self) -> None: ...

  def parse_line(self, line: str) -> None:
    ...  # Vars, tasks, commands. Simple right?

    self.line += 1  # Last!

  def parse_script(self, code: str) -> None:
    lines = code.split('\n')

    for line in lines:
      self.parse_line(line)
