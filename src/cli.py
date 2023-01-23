from ansi import Ansi
from interpreter.flags import Flags
from interpreter.runner import Runner
from os import getcwd, scandir
from out import BuildDocError, BuildDocSuccess
from sys import exit


VERSION = "0.0.0"


class Cli:
    """ Handles the CLI stuff. """

    FLAGS: list[tuple[str, str]] = [
        ("--help", "Displays help."),
        ("--version", "Displays version."),
        ("--always-zero", "Prevents BuildDoc from exiting with any status code other than zero."),
        ("--no-echo", "Prevents BuildDoc from echoing the command being run regardless of silence operator."),
        ("--verbose", "Enable verbose output.")]
    args: list[str]

    def __init__(self, args: list[str]) -> None: self.args = args

    def help(self) -> None: print("Flags:"); [print(f"{f}  {d}") for f, d in self.FLAGS]; exit(0)

    def read_flags(self, _flags: list[str] | None) -> dict[str, bool]:
        """ Checks the given flags and gives them to the parser & runner. """
        flags: dict[str, bool] = {}

        if _flags is not None:
            for f in _flags:
                match f[2:]:
                    case "help": self.help()
                    case "version": print(f"BuildDoc {Ansi.special.SUCCESS}v{VERSION}{Ansi.special.RESET}"); exit(0)
                    case "always-zero": flags["always_zero"] = True
                    case "no-echo": flags["no_echo"] = True
                    case "verbose": flags["verbose"] = True
                    case _: raise BuildDocError("unknown flag: '%s'" %f, 1)

        return flags

    def builddoc_path(self) -> str | None:
        CWD = getcwd()
        PATH = [f"{CWD}/{file.name}" for file in scandir(CWD) if file.name.lower() == "builddoc"]
        return PATH[0] if len(PATH) > 0 else None

    def process(self) -> None:
        PATH = self.builddoc_path()
        task = self.args[1] if len(self.args) >= 2 and not self.args[1][0] == '-' else None
        cli_flags = [f for f in self.args if f[:2] == '--'] if len(self.args) >= 2 else None
        flags = Flags(cli_flags)

        if flags.display_help:
            print(f"Usage: {Ansi.style.LIGHT}build [options] & [task] | [options] | [task]{Ansi.special.RESET}",
                f"\nOptions: {Ansi.style.LIGHT}--allow-recursion | --always-zero | --no-echo | --verbose | --help | --init{Ansi.special.RESET}")

        elif flags.init:
            with open("BuildDoc", 'w') as builddoc:
                TEXT = ["# Variables go up here.\n", "[main]", "echo \"Works!\""]

                [builddoc.write("%s\n" %line) for line in TEXT]
                builddoc.close()

                BuildDocSuccess("created './BuildDoc'!")

        else:
            if PATH is not None:
                with open(PATH, 'r') as builddoc:
                    try: Runner.run_task(builddoc.readlines(), task, flags)
                    except IndexError: ...
            else: raise BuildDocError("no builddoc found", 0 if flags.always_zero else 1)
