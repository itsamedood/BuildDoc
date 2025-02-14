from interpreter.command import Command
from interpreter.flags import Flags
from interpreter.variable import Variable
from out import BuildDocDebugMessage, BuildDocError


class VariableManager:
  """
  Holds all variables for BuildDoc,
  including ones from a `.env` and ones declared in the script.
  """

  reg: dict[str, tuple[Variable, int]] = {}
  env: dict[str, Variable] = {}

  def __init__(self) -> None: ...

  def get_reg(self, _var: str) -> tuple[Variable, int]:
    if _var not in self.reg: raise BuildDocError("%s not declared." %_var, 1)
    var, line = self.reg[_var]
    return (var, line)

  def get_env(self, _var: str) -> Variable:
    if _var not in self.env: raise BuildDocError("%s not declared." %_var, 1)
    return self.env[_var]

  def print_vars(self, _reg = True, _env = True):
    if _reg:
      for v in self.reg:
        var, line = self.reg[v]
        print(f"[R] {v} = {var.value} ({line})")

    if _env: [print(f"[E] {v} = {self.env[v].value}") for v in self.env]


class AST:
  """
  Abstract Syntax Tree. Keeps track of variables, tasks, etc.
  """

  def __init__(self, _flags: Flags, _vm: VariableManager) -> None:
    self.FLAGS = _flags
    self.VARIABLES = _vm
    self.TASKS: dict[str, list[Command]] = {}

  def print_vars(self) -> None: return self.VARIABLES.print_vars()

  def print_tasks(self) -> None:
    [BuildDocDebugMessage("%s =" %task_name, [t.cmd for t in self.TASKS[task_name]], _verbose=self.FLAGS.verbose) for task_name in self.TASKS]

  def print_commands(self) -> None:
    # Condensed with list comprehension (I was bored..)
    [[BuildDocDebugMessage(c.cmd, _verbose=self.FLAGS.verbose) for c in self.TASKS[task]] for task in self.TASKS]
