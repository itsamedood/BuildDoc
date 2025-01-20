from enum import Enum
from os import getcwd
from os.path import exists
from out import Ansi, BuildDocError, BuildDocSuccess, BUILDDOC_VERSION
from platform import system
from sys import exit


class OS(Enum):
  WINDOWS = "Windows"
  MACOS = "Darwin"
  LINUX = "Linux"


class Flags:
  """ Represents flags passed in through the command line. """

  USAGE = "Usage: build [flags] [task]"

  # tuple[str, str] = Flag name, shorthand name (version, v).
  # str = Flag description.
  # int = Amount of spaces to add to keep all the `|` aligned.
  groupings: list[tuple[tuple[str, str], str, int]] = [
    (("verbose", "vb"), "Prints debug stuff.", 1),
    (("help", 'h'), "Displays this menu.", 4),
    (("version", 'v'), "Displays version.", 1),
    (("init", 'i'), "Creates a BuildDoc template.", 4),
    (("ace", 'a'), "Allows Fang operators which grant ACE (Arbitrary Code Execution).", 5)
  ]

  def __init__(self, _flags: list[str]):
    self.verbose = False
    self.ace = False
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
          helpl: list[str] = [self.USAGE, "Flags:"]

          for (name, shorthand), description, spaces in self.groupings:
            firstspaces = ''.join([' ' for _ in range(spaces)])
            secspaces = ''.join([' ' for _ in range(3 if len(shorthand) == 1 else 2)])  # Second set of spaces.
            # Indent 2 spaces.
            helpl.append(f"  -{name}{firstspaces}| -{shorthand}{secspaces}| {description}")

          print('\n'.join(helpl))
          exit(0)

        case "version" | 'v':
          print(f"""BuildDoc {Ansi.style.LIGHT}v{BUILDDOC_VERSION}{Ansi.special.RESET}
© David Spencer Jr.
""")
          exit(0)

        case "init" | 'i':  # Creates a template BuildDoc in $PWD.
          if not exists(path:="%s/BuildDoc" %self._PWD):
            with open(path, 'x') as builddoc:
              TEMPLATE = [
                "# Variables go here.\n",
                "# `build` run the first task in the script by default (`run` in this case)."
                "# To specify a task to run, run `build <task>`.",
                "[run]",
                "echo \":)\""
              ]

              builddoc.write('\n'.join(TEMPLATE))
              builddoc.close()

            BuildDocSuccess("created %s/BuildDoc!" %self._PWD)
            exit(0)
          else: raise BuildDocError("%s already exists!" %path, 1)

        case "ace" | 'a': self.ace = True

        case badflag:
          BuildDocError("BuildDoc flags use 1 `-`!" if badflag[0] == '-' else "%s isn't a flag; run `build -help` for valid flags." %badflag, 1)
