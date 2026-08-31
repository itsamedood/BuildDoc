from enum import Enum
from platform import system


class OS(Enum):
  WINDOWS = "Windows"
  MACOS   = "Darwin"
  LINUX   = "Linux"


class Flags:
  """ Represents flags for BuildDoc. """

  USAGE = "Usage: build [-flags] [task]"

  # tuple[str, str] 👉 Flag, shorthand (help, h)
  # str, int 👉 Description, spaces to keep `|`s aligned.
  groupings: list[tuple[tuple[str, str], str, int]] = [
    (("help", 'h'), "Displays this menu.", 4),
    (("verbose", 'v'), "Prints debug stuff.", 1),
    (("init", 'i'), "Creates a BuildDoc template.", 4),
    (("version", 'v'), "Displays installed version.", 1)
  ]

  def __init__(self, flags: list[str]) -> None:
    self.verbose = False
    self.as_list = flags

    try: self.os = OS(system())
    except ValueError: raise
