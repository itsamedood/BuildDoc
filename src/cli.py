from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runner import Runner
from out import BuildDocError
from ansi import Ansi
from os.path import exists, curdir
from sys import exit


VERSION = "0.0.0"


class Cli:
    """ Handles the CLI stuff. """

    FLAGS: list[tuple[str, str]] = [
        ("--help", "Displays help."),
        ("--version", "Displays version."),
        ("--always-zero", "Prevents BuildDoc from exiting with any status code other than zero."),
        ("--no-echo", "Prevents BuildDoc from echoing the command being run regardless of silence operator.")]
    args: list[str]

    def __init__(self, args: list[str]) -> None: self.args = args

    def help(self) -> None: print("Flags:"); [print(f"{t[0]}  {t[1]}") for t in self.FLAGS]; exit(0)

    def read_flags(self, _flags: list[str] | None) -> dict[str, bool]:
        """ Checks the given flags and gives them to the parser & runner. """
        flags: dict[str, bool] = {}

        always_zero, no_echo = False, False

        if _flags is not None:
            for f in _flags:
                match f[2:]:
                    case "help": self.help()
                    case "version": print(f"BuildDoc {Ansi.special.SUCCESS}v{VERSION}{Ansi.special.RESET}"); exit(0)
                    case "always-zero": always_zero = True
                    case "no-echo": no_echo = True
                    case f: raise BuildDocError(f"unknown flag: '{f}'", 1)

        flags["always-zero"] = always_zero
        flags["no-echo"] = no_echo
        return flags

    def process(self) -> None:
        task = self.args[1] if len(self.args) >= 2 and not self.args[1][0] == '-' else None
        flags = [f for f in self.args if f[:2] == '--'] if len(self.args) >= 2 else None

        if exists(f"{curdir}/builddoc"):
            with open(f"{curdir}/builddoc", 'r') as builddoc:
                read_flags = self.read_flags(flags)
                always_zero, no_echo = read_flags["always-zero"], read_flags["no-echo"]


                Runner.run_task(no_echo, task, Parser(always_zero).map(Lexer.tokenize(builddoc.readlines())[1:]))
        else: raise BuildDocError("no builddoc found", 1)
