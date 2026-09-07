from interpreter.token import Token  # Sleepy?
from typing import Any


class Parser:
  """ Parses the tokens from the lexer. This is the messy part. """

  line, character = 0, 0
  variables: list[tuple[str, Any]]

  def __init__(self) -> None: ...

  def parse_line(self) -> None: ...
