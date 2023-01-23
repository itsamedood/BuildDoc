from ansi import Ansi
from sys import exit
from typing import Any


class BuildDocError(BaseException):
    """ Base class for all BuildDoc errors. """
    def __init__(self, message: str, code: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: {message}.")
        exit(code)


class BuildDocTracedError(BuildDocError):
    """ Error with a trace to the line & character. """
    def __init__(self, message: str, code: int, line: int, char: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: [{Ansi.style.LIGHT}{line}{Ansi.special.RESET},{Ansi.style.LIGHT}{char}{Ansi.special.RESET}]: {message}.")
        exit(code)


class BuildDocWarning:
    """ Represents a warning in BuildDoc. """
    def __init__(self, message: str) -> None: print(f"builddoc: {Ansi.special.WARNING}warning{Ansi.special.RESET}: {message}.")


class BuildDocTracedWarning:
    """ Represents a warning with a trace in BuildDoc. """
    def __init__(self, message: str, line: int, char: int) -> None: print(f"builddoc: {Ansi.special.WARNING}warning{Ansi.special.RESET}: [{Ansi.text.BLACK}{line}{Ansi.special.RESET},{Ansi.text.BLACK}{char}{Ansi.special.RESET}]: {message}.")


class BuildDocNote:
    """ Represents a note from the BuildDoc interpreter. """
    def __init__(self, message: str) -> None: print(f"builddoc: {Ansi.special.NOTE}note{Ansi.special.RESET}:", message)


class BuildDocSuccess:
    def __init__(self, message: str) -> None:
        print(f"builddoc: {Ansi.special.SUCCESS}success{Ansi.special.RESET}: {message}")
        exit(0)


class BuildDocDebugMessage:
    """ A message from the interpreter when debugging. """
    def __init__(self, message: str) -> None: print(f"builddoc: {Ansi.style.BOLD}{Ansi.text.YELLOW}{Ansi.bg.YELLOW}debug{Ansi.special.RESET}: {message}")
