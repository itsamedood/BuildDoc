from enum import Enum
from platform import system


class OS(Enum):
  WINDOWS = "Windows"
  MACOS   = "Darwin"
  LINUX   = "Linux"


class Flags:
  """ Represents flags for BuildDoc. """

  USAGE = "Usage: build [-flags] [task] | build [-help|-h]"
  BUILDDOC_VERSION = "0.0.1"

  # tuple[str, str | None] 👉 Flag, shorthand (help, h). If shorthand is None it doesn't have one, duh.
  # str 👉 Description
  # tuple[int, int] 👉 spaces to keep both `|`s aligned.
  groupings: list[tuple[tuple[str, str | None], str, tuple[int, int]]] = [
    (("help", 'h'), "Displays this menu.", (4, 4)),
    (("verbose", 'v'), "Prints debug stuff.", (1, 4)),
    (("init", 'i'), "Creates a BuildDoc template.", (4, 4)),
    (("version", None), "Displays installed version.", (1, 8))
  ]

  task: str | None = ''  # Not really necessary but maybe you'll want the task given at runtime? Idk.
  givens: dict[str, bool] = {
    "verbose": False,
    # ...
  }

  def __init__(self, argv: list[str]) -> None:
    self.task = last if (last:=argv[-1])[0] != '-' else None  # hehe pp operator.

    for oarg in argv:
      if not oarg[0] == '-': continue
      arg = oarg[1:]

      if arg == 'help' or arg == 'h':
        self.show_help()
        exit(0)

      if arg == 'version':
        print("BuildDoc - itsamedood | v%s" %self.BUILDDOC_VERSION)
        exit(0)

      ...  # Update givens dict.

    try: self.os = OS(system())
    except ValueError: raise

  def show_help(self) -> None:
    print(self.USAGE, "Flags:", sep='\n')

    for group in self.groupings:
      name, shorthand = group[0]
      desc = group[1]
      firstspaces, secondspaces = group[2]

      print(f"  {f"{name}{' '*firstspaces}| {shorthand}" if not shorthand is None else f"{name}"}{' '*secondspaces}| {desc}")
