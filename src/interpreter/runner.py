from interpreter.command import Command
from interpreter.evaluator import Evaluator
from interpreter.flags import Flags
from os import system
from out import BuildDocError


class Runner:
  """ Responsible for running commands in a task and reporting any failed commands. """

  def __init__(self, _flags: Flags) -> None:
    self.FLAGS = _flags
    self.evaluator = Evaluator(_flags)

  def run_task(self, _task: str, _commands: list[Command]):
    if len(_commands) < 1: raise BuildDocError("no commands to execute for task '%s'." %_task, 1)

    in_if = False

    for cmdobj in _commands:
      cmd = cmdobj.cmd
      if cmd[:2] == "if":
        in_if = True
        continue

      elif cmd == "else": ...
      elif cmd == "endif": ...

      if in_if: ...

      if not cmdobj.silent: print(cmd)
      retval = system(cmd[1:] if cmdobj.silent else cmd)

      if retval > 0: raise BuildDocError(f"command '{cmd}' exited with code {retval}.", retval)
