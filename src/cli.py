from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runner import Runner
from out import BuildDocError
from ansi import Ansi
from os.path import exists, curdir


class Cli:
    """
    Handles the CLI stuff.
    """

    CMDS = ["-h", "-v"]
    args: list[str]

    def __init__(self, args: list[str]) -> None:
        self.args = args
        pass

    def help(self) -> None:
        return print("Commands:\n", "\n ".join([cmd for cmd in self.CMDS]))

    def process_args(self):
        arg = self.args[1] if len(self.args) >= 2 else None
        args = self.args[2:] if len(self.args) >= 3 else None

        match arg:
            case "-h":  # Help.
                if args is None:
                    return self.help()
                else:
                    raise BuildDocError("too many arguments", 0)

            case "-v":  # Version.
                return print(f"BuildDoc {Ansi.special.SUCCESS}v0.0.1{Ansi.special.RESET}")

            case task:  # The task to run (None = default).
                if exists(f"{curdir}/builddoc"):
                    with open(f"{curdir}/builddoc", "r") as builddoc:
                        Runner.run_task(task, Parser.map(Lexer.tokenize(builddoc.readlines())[1:]))  # 😎
                else:
                    raise BuildDocError("No BuildDoc found.", 1)
