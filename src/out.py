from ansi import Ansi
from inspect import currentframe, getouterframes
from pathlib import Path
from sys import exit
from typing import Any


parse_filename = lambda name: name.split('\\')[-1].split('/')[-1]  # `name` should be `str`.
clear_strios = lambda *strios: [sio.seek(0) or sio.truncate(0) for sio in strios]  # `strios` should be `StringIO`.


class Logger:
  """
  Handles logging debug stuff to `builddoc.log`.
  """

  path = Path.cwd() / "builddoc.log"

  @staticmethod
  def create_log() -> None: return Logger.path.touch(exist_ok=True)

  @staticmethod
  def check_for_log() -> bool: return Logger.path.exists()

  @staticmethod
  def write_to_log() -> None:
    Logger.create_log()


  # @staticmethod
  # def check_for_log() -> bool: return Logger.path.exists()



class BuildDocError(BaseException):
  """ Base class for all BuildDoc errors. """

  def __init__(self, message: str, code: int) -> None:
    print(f"builddoc: {Ansi.preset.ERROR}error{Ansi.preset.RESET}: {message}")
    exit(code)


class BuildDocInternalTracedError(BuildDocError):
  """
  Interal error with a trace to the line and file that caused it.
  For debug purposes, so hopefully you never see it!
  """

  def __init__(self, message: str, code: int) -> None:
    caller = getouterframes(currentframe(), 2)[1]

    print(f"builddoc: {Ansi.preset.ERROR}INTERNAL ERROR{Ansi.preset.RESET}: (line {Ansi.style.LIGHT}{caller.lineno}{Ansi.preset.RESET} in {Ansi.style.LIGHT}{parse_filename(caller.filename)}{Ansi.preset.RESET}): {message}")
    exit(code)


class BuildDocTracedError(BuildDocError):
  """  Error with a trace to the line and character that caused it. """

  def __init__(self, message: str, code: int, line: int, char: int) -> None:
    print(f"builddoc: {Ansi.preset.ERROR}error{Ansi.preset.RESET}: [{Ansi.style.LIGHT}{line}{Ansi.preset.RESET},{Ansi.style.LIGHT}{char}{Ansi.preset.RESET}]: {message}")
    exit(code)


class BuildDocWarning:
  """ Just a warning, nothing fatal but you shouldn't ignore. """
  def __init__(self, message: str) -> None: print(f"builddoc: {Ansi.preset.WARNING}warning{Ansi.preset.RESET}: {message}")


# class BuildDocTracedWarning: ...


class BuildDocSuccess:
  """ Lil' success message. """
  def __init__(self, message: str) -> None: print(f"builddoc: {Ansi.preset.SUCCESS}success{Ansi.preset.RESET}: {message}")


class BuildDocDebugMessage:
  """ A message from the interpreter that stands out more. """

  def __init__(self, *values: Any) -> None:
    caller = getouterframes(currentframe(), 2)[1]

    # Display message, then all values ended with `\n`.
    print(f"builddoc: {Ansi.preset.DEBUG}DEBUG{Ansi.preset.RESET} (line {Ansi.style.LIGHT}{caller.lineno}{Ansi.preset.RESET} in {Ansi.style.LIGHT}{parse_filename(caller.filename)}{Ansi.preset.RESET}):", end=' ')
    [print(v, end='\n') if i == len(values)-1 else print(v, end=' ') for i, v in enumerate(values)]
