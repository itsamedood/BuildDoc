# ANSI Classes.
class TextStyle:
  NORMAL      = "\033[0m"
  BOLD        = "\033[1m"
  LIGHT       = "\033[2m"
  ITALIC      = "\033[3m"
  UNDERLINE   = "\033[4m"
  BLINK       = "\033[5m"


class TextColor:
  BLACK     = "\033[0;30m"
  RED       = "\033[0;31m"
  GREEN     = "\033[0;32m"
  YELLOW    = "\033[0;33m"
  BLUE      = "\033[0;34m"
  PURPLE    = "\033[0;35m"
  CYAN      = "\033[0;36m"
  WHITE     = "\033[0;37m"


class BGColor:
  BLACK     = "\033[0;40m"
  RED       = "\033[0;41m"
  GREEN     = "\033[0;42m"
  YELLOW    = "\033[0;43m"
  BLUE      = "\033[0;44m"
  PURPLE    = "\033[0;45m"
  CYAN      = "\033[0;46m"
  WHITE     = "\033[0;47m"


class Preset:
  ERROR     = "\033[1;31m"
  SUCCESS   = "\033[1;32m"
  WARNING   = "\033[1;33m"
  DEBUG     = "\033[1;37;43m"
  NOTE      = "\033[1;47m"
  RESET     = "\033[0;0;0m"


class Ansi:
  """ Class for easily using ANSI color codes! """

  style = TextStyle()
  text = TextColor()
  bg = BGColor()
  preset = Preset()


  @staticmethod
  def new(style: int, text_col: int, bg_col: int) -> str: return f"\033[{style};{text_col};{bg_col}m"
