from out import BuildDocError, BuildDocSuccess
from pathlib import Path
from sys import argv


# class OS(Enum):
#   WINDOWS = "Windows"
#   MACOS   = "Darwin"
#   LINUX   = "Linux"


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
    (("log", 'l'), "Log everything to a log file for debugging.", (5, 4)),
    (("init", None), "Creates a BuildDoc template.", (4, 11)),
    (("version", None), "Displays installed version.", (1, 8))
  ]

  task: str | None = ''  # Not really necessary but maybe you'll want the task given at runtime? Idk.
  givens: dict[str, bool] = {
    "verbose": False,
    # ...
  }

  @staticmethod
  def init() -> None:
    """ Initializes the class itself, because it's static. """

    Flags.task = last if (last:=argv[-1])[0] != '-' else None  # hehe pp operator.

    for oarg in argv:
      if not oarg[0] == '-': continue
      arg = oarg[1:]

      if arg == 'help' or arg == 'h':
        Flags.show_help()
        exit(0)

      if arg == 'init':
        if ((fullpath:=Path().cwd()/"BuildDoc").exists()): raise BuildDocError("`%s` already exists." %fullpath, 1)

        fullpath.touch()
        with open(fullpath, 'w') as initdfile:
          initdfile.write("# Created using `build -init`!\n\nMAIN=\"src/main.py\"\nPYFLAGS=\"-B\"\n\n[run]\npython3 $PYFLAGS $MAIN")

        BuildDocSuccess("Created `%s`!" %fullpath)
        exit(0)

      if arg == 'version':
        print("BuildDoc - itsamedood | v%s" %Flags.BUILDDOC_VERSION)
        exit(0)


      # Really didn't wanna do a nested loop but oh well.
      for group in Flags.groupings:
        name, shorthand = group[0]
        if arg == name or arg == shorthand: Flags.givens[name] = True
    ...

  @staticmethod
  def show_help() -> None:
    print(Flags.USAGE, "Flags:", sep='\n')

    for group in Flags.groupings:
      name, shorthand = group[0]
      desc = group[1]
      firstspaces, secondspaces = group[2]

      print(f"  {f"{name}{' '*firstspaces}| {shorthand}" if not shorthand is None else f"{name}"}{' '*secondspaces}| {desc}")
