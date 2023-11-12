from interpreter.flags import Flags
from interpreter.interpreter import Interpreter
from os import getcwd, scandir
from out import BuildDocError


class Cli:
  def __init__(self, argv: list[str]) -> None:
    self.FLAGS = Flags([a[1:] for a in argv if a[0] == '-' and len(a) > 1])
    self.ARGS = [a for a in argv]
    self.CWD = getcwd()

  def process_args(self):
    task = None
    if len(self.ARGS) > 1 and not self.ARGS[-1][0] == '-': task = self.ARGS[-1]
    print(self.ARGS)

    try:
      global path
      path = [f"{self.CWD}/{f.name}" for f in scandir(self.CWD) if f.name.lower() == "builddoc"][0]
    except IndexError: raise BuildDocError("BuildDoc not found.", 1)

    intrptr = Interpreter(self.FLAGS)
    intrptr.interpret(path, task)
