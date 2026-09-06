from interpreter.lexer import Lexer
from out import BuildDocDebugMessage
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
    tokens = self.lexer.tokenize(self.code)
    BuildDocDebugMessage([f"{t.name}, {v}" for t,v in tokens])

    # Parser!
    ...
