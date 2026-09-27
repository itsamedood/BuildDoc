from interpreter.lexer import Lexer
from interpreter.parser import Parser
from out import BuildDocDebugMessage
from pathlib import Path


class Interpreter:
  """
  Handles invoking the lexer and parser.
  """

  lexer = Lexer()
  parser = Parser()

  def __init__(self, path: Path) -> None:
    with open(path, "r") as script:
      self.code = script.read()

    # Lexer!
    tokens = self.lexer.tokenize(self.code)
    BuildDocDebugMessage([f"{t.name}, {v}" for t,v in tokens])

    # Parser!
    self.parser.parse_script(self.code)
