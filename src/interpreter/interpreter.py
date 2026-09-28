from interpreter.lexer import Lexer
from interpreter.parser import Parser
from out import BuildDocDebugMessage
from pathlib import Path


class Interpreter:
  """
  Handles invoking the lexer and parser.
  """

  def __init__(self, path: Path) -> None:
    with open(path, "r") as script:
      self.code = [line.strip() for line in script.readlines()]

    # Lexer!
    # self.lexer = Lexer()
    # self.parser = Parser((tokens:=self.lexer.tokenize(self.code)))
    self.parser = Parser(tokens:=((lexer:=Lexer()).tokenize(self.code)))  # God I love walrus operator.
    self.tokens, self.lexer = tokens, lexer

    # BuildDocDebugMessage([[f"{t.name}, {v}" for t,v in lt] for lt in tokens])

    # Parser!
    self.parser.parse_script(tokens)
