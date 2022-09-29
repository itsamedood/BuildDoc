from ansi import Ansi


class BuildDocError(BaseException):
    """
    Base class for all BuildDoc errors.
    """
    def __init__(self, message: str, code: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: {message}.")
        exit(code)

class BuildDocTracedError(BuildDocError):
    """
    Error with a trace to the line & character.
    """

    def __init__(self, message: str, code: int, line: int, char: int) -> None:
        print(f"builddoc: {Ansi.special.ERROR}error{Ansi.special.RESET}: [{Ansi.text.BLACK}{line}{Ansi.special.RESET},{Ansi.text.BLACK}{char}{Ansi.special.RESET}]: {message}.")
        exit(code)
