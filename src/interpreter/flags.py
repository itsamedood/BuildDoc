from enum import Enum
from os import getenv
from out import Ansi, BuildDocError, BuildDocSuccess, BUILDDOC_VERSION
from platform import system
from sys import exit


class OS(Enum):
    WINDOWS = "Windows"
    MACOS = "Darwin"
    LINUX = "Linux"


class Flags:
    """ Represents flags passed in through the command line. """

    def __init__(self, _flags: list[str]):
        self.allow_recursion = False
        self.debug = False
        self.verbose = False
        self.as_list = _flags
        self._OS = None

        os = system()
        try: self._OS = OS(os)
        except ValueError: raise BuildDocError("unknown OS.", 0 if self.debug else 1)

        self._PWD = getenv("PWD") if self._OS == OS.LINUX or self._OS == OS.MACOS else getenv("CWD")
        if self._PWD is None: raise BuildDocError("couldn't get PWD.", 0 if self.debug else 1)

        for flag in _flags:
            match flag:
                case "allow-recursion" | "ar": self.allow_recursion = True  # Determines if a task is allowed to call itself.
                case "verbose" | "vb": self.verbose = True  # Prints extra info, mostly for debugging.
                case "debug" | 'd': self.debug = True  # If true, the program will always exit with status code `0`.

                case "help" | 'h':  # Displays help text.
                    HELP = [
                        # "BuildDoc",
                        "Usage: build [flags] [task]",
                        "Flags:",
                        "╭─ -allow-recursion | -ar",
                        "⏐  -verbose         | -vb",
                        "⏐  -debug           | -d",
                        "⏐  -help            | -h",
                        "⏐  -version         | -v",
                        "╰─ -init            | -i",
                    ]

                    [print(l) for l in HELP]; exit(0 if self.debug else 1)

                case "version" | 'v': print(f"BuildDoc {Ansi.style.LIGHT}v{BUILDDOC_VERSION}{Ansi.special.RESET}")

                case "init" | 'i':  # Creates a template BuildDoc in $PWD.
                    with open("%s/BuildDoc" %self._PWD, 'x') as builddoc:
                        TEMPLATE = [
                            "# Variables go here.\n",
                            "[main] # Main task, run by default.",
                            "echo \":)\""
                        ]

                        builddoc.write('\n'.join(TEMPLATE))
                        builddoc.close()

                    BuildDocSuccess("created %s/BuildDoc!" %self._PWD)
                    exit(0)
