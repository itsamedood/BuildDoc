from interpreter.command import Command
from interpreter.flags import Flags
from interpreter.variable import Variable
from out import BuildDocDebugMessage


class AST:
  """
  Abstract Syntax Tree. Keeps track of variables, tasks, etc.
  """

  def __init__(self, _flags: Flags) -> None:
    self.FLAGS = _flags
    self.VARIABLES: dict[str, Variable] = {}
    self.TASKS: dict[str, list[Command]] = {}

  def print_vars(self) -> None:
    for var_name in self.VARIABLES:
      var_type = self.VARIABLES[var_name].type.name[0]  # 'R' || 'E'
      BuildDocDebugMessage(f"[{var_type}] {var_name} =", self.VARIABLES[var_name].value, _verbose=self.FLAGS.verbose)

  def print_tasks(self) -> None:
    for task_name in self.TASKS:
      BuildDocDebugMessage("%s =" %task_name, [t.cmd for t in self.TASKS[task_name]], _verbose=self.FLAGS.verbose)

  def print_commands(self) -> None:
    for task in self.TASKS: [c.cmd for c in self.TASKS[task]]
