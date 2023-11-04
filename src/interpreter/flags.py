from enum import Enum
from os import getcwd
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
    self.verbose = False
    self.as_list = _flags
    self._OS = None

    os = system()
    try: self._OS = OS(os)
    except ValueError: raise BuildDocError("unknown OS.", 1)

    self._PWD = getcwd()
    if self._PWD is None: raise BuildDocError("couldn't get PWD.", 1)

    for flag in _flags:
      match flag:
        case "verbose" | "vb": self.verbose = True  # Prints extra info, mostly for debugging.

        case "help" | 'h':  # Displays help text.
          HELP = [
            # "BuildDoc",
            "Usage: build [flags] [task]",
            "Flags:",
            "  -verbose | -vb",
            "  -help  | -h",
            "  -version | -v",
            "  -init  | -i",
          ]

          [print(l) for l in HELP]
          exit(0)

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
