from interpreter.token import Token
from pathlib import Path
from typing import Iterator


class Lexer:
  """
  Tokenizes the script into tokens for the parser. Ignores comments.
  """

  def __init__(self) -> None: ...

  # Tokenizes code into an iterator to yield later for O(1) time.
  def tokenize(self, code: bytes) -> Iterator[Token]:
    ...
