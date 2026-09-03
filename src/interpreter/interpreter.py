from interpreter.lexer import Lexer
from pathlib import Path


class Interpreter:
  """
  Handles invoking the lexer and parser.
  """

  lexer = Lexer()

  def __init__(self, path: Path) -> None:
    with open(path, "r") as script:
      self.code = script.read()

    # Lexer!
    self.lexer.tokenize(self.code)

    # Parser!
    ...
