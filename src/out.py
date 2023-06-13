from sys import exit


BUILDDOC_VERSION = "0.0.0"


# ANSI classes.
class TextStyle:
    NORMAL      = "\033[0m"
    BOLD        = "\033[1m"
    LIGHT       = "\033[2m"
    ITALICIZED  = "\033[3m"
    UNDERLINED  = "\033[4m"
    BLINK       = "\033[5m"


class TextColor:
    BLACK   = "\033[0;30m"
    RED     = "\033[0;31m"
    GREEN   = "\033[0;32m"
    YELLOW  = "\033[0;33m"
    BLUE    = "\033[0;34m"
    PURPLE  = "\033[0;35m"
    CYAN    = "\033[0;36m"
    WHITE   = "\033[0;37m"


class BGColor:
    BLACK   = "\033[0;40m"
    RED     = "\033[0;41m"
    GREEN   = "\033[0;42m"
    YELLOW  = "\033[0;43m"
    BLUE    = "\033[0;44m"
    PURPLE  = "\033[0;45m"
    CYAN    = "\033[0;46m"
    WHITE   = "\033[0;47m"


class Special:
    SUCCESS = "\033[1;32m"
    WARNING = "\033[1;33m"
    ERROR   = "\033[1;31m"
    NOTE    = "\033[1;47m"
    RESET   = "\033[0;0;0m"


class Ansi:
    """ Class for using ANSI color codes. """
    style   = TextStyle()
    text    = TextColor()
    bg      = BGColor()
    special = Special()


    @staticmethod
    def new(style: int, text_color: int, bg_color: int) -> str:
        """ Creates a new ANSI color code. If the numbers are not valid, the effect is not produced. """
        if text_color and bg_color == 0: return "\033[%sm" %style
        return f"\033[{style};{bg_color}m" if text_color == 0 else f"\033[{style};{text_color}m"



# Error classes.
class BuildDocError(BaseException):
    """ Base class for all BuildDoc errors. """
    def __init__(self, message: str, code: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: {message}")
        exit(code)


class BuildDocTracedError(BuildDocError):
    """ Error with a trace to the line & character. """
    def __init__(self, message: str, code: int, line: int, char: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: [{Ansi.style.LIGHT}{line}{Ansi.special.RESET},{Ansi.style.LIGHT}{char}{Ansi.special.RESET}]: {message}.")
        exit(code)


class BuildDocMacroError(BuildDocError):
    def __init__(self, macro_name: str, message: str, code: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: ({Ansi.style.LIGHT}%{macro_name}{Ansi.special.RESET}): {message}.")
        exit(code)

class BuildDocMacroArgumentError(BuildDocMacroError):
    def __init__(self, macro_name: str, expected: int, got: int, code: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: ({Ansi.style.LIGHT}%{macro_name}{Ansi.special.RESET}): expected {expected} argument(s); got {got}.")
        exit(code)


class BuildDocWarning:
    """ Represents a warning in BuildDoc. """
    def __init__(self, message: str) -> None: print(f"builddoc: {Ansi.special.WARNING}warning{Ansi.special.RESET}: {message}")


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
