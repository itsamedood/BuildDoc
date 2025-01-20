from interpreter.ast import AST
from interpreter.command import Command
from interpreter.evaluator import Evaluator
from interpreter.flags import Flags
from os import system
from out import BuildDocDebugMessage, BuildDocError


class Runner:
  """
  Responsible for running commands in a task and reporting any failed commands.

  This is the class that `self` will refer to when using either of the fang operators (`~<`|`~^`).
  """

  def __init__(self, _flags: Flags, _ast: AST) -> None:
    self.FLAGS = _flags
    self.TREE = _ast
    self.VM = _ast.VARIABLES
    self.evaluator = Evaluator(_flags)

  def run_task(self, _task: str, _commands: list[Command]):
    if len(_commands) < 1: raise BuildDocError("no commands to execute for task '%s'." %_task, 1)

    in_if = False

    for cmdobj in _commands:
      cmd = cmdobj.cmd

      # Stupid spaghetti code parser, I'll handle Fang operators here.
      if cmd[:2] == "~<" and self.FLAGS.ace:  # Eval Fang.
        BuildDocDebugMessage("Arbitrary code: %s" %(ac:=cmd[3:]), _verbose=self.FLAGS.verbose)
        eval(ac)
        continue

      if cmd[:2] == "~^" and self.FLAGS.ace:  # Exec Fang.
        BuildDocDebugMessage("Arbitrary code: %s" %(ac:=cmd[3:]), _verbose=self.FLAGS.verbose)
        exec(ac)
        continue

      if cmd[:2] == "if":
        in_if = True
        continue

      elif cmd == "else": ...
      elif cmd == "endif": ...

      if in_if: ...

      if not cmdobj.silent: print(cmd)
      retval = system(cmd[1:] if cmdobj.silent else cmd)

      if retval > 0: raise BuildDocError(f"command '{cmd}' exited with code {retval}.", retval)
