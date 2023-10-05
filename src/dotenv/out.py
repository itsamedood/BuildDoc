from out import Ansi


class DotEnvError(BaseException):
    frmt = f"builddoc -> {Ansi.text.YELLOW}dotenv{Ansi.special.RESET}:"

    def __init__(self, _message: str, _code: int) -> None:
        print(f"{self.frmt} {_message}")
        exit(_code)


class DotEnvTracedError(DotEnvError):
    def __init__(self, _message: str, _code: int, _line: int, _char: int) -> None:
        self.frmt += f"[{Ansi.style.LIGHT}{_line}{Ansi.special.RESET}:{Ansi.style.LIGHT}{_char}{Ansi.special.RESET}]:"
        super().__init__(_message, _code)
