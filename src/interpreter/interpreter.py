from interpreter.ast import VariableManager
from interpreter.evaluator import Evaluator
from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runner import Runner
from os import getenv
from out import BuildDocError


class Interpreter:
  """ Easier way to call everything in order for BuildDoc to work properly. """

  def __init__(self, _flags: Flags) -> None:
    self.PWD = getenv("PWD")
    self.FLAGS = _flags
    self.lexer = Lexer(_flags)
    self.parser = Parser(_flags, VariableManager(), evaluator:=Evaluator(_flags))
    # self.runner = Runner(_flags)
    self.evaluator = evaluator

  def interpret(self, _path: str, _task: str | None):
    with open(_path, 'r') as builddoc:
      code = builddoc.read()
      self.TREE = self.parser.parse_tokens(self.lexer.tokenize(code))

      if _task is None: _task = [t for t in self.TREE.TASKS][0]
      if _task not in self.TREE.TASKS: raise BuildDocError("no task found named '%s'." %_task, 1)

      if self.FLAGS.verbose:
        self.TREE.print_vars()
        self.TREE.print_tasks()
        self.TREE.print_commands()

      self.runner = Runner(self.FLAGS, self.TREE)
      self.runner.run_task(_task, self.TREE.TASKS[_task])
