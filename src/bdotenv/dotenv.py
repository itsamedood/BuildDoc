from interpreter.variable import *
from bdotenv.out import DotEnvError, DotEnvTracedError
from io import StringIO
from re import match
from os import getcwd, scandir

from out import BuildDocDebugMessage


class DotEnv:
  def read(self) -> dict[str, Variable]:
    """ Reads all `.env` files in the current working directory. """

    pairs: dict[str, Variable] = {}
    got: dict[str, tuple[Variable, int, int]] = {}  # Var, line, char value started at.
    dotenv_files = [e for e in scandir(getcwd()) if e.is_file() and e.name[-4:] == ".env"]

    name, value = StringIO(), StringIO()
    line, char = 1, 0
    ignore, reading_value = False, False

    if not len(dotenv_files) > 0: return {}

    for dotenv_file in dotenv_files:
      with open(dotenv_file.path, 'r') as dotenv:
        lines = dotenv.read()

        # Read through and just get vars and their values.
        for c in lines:
          char += 1
          if c == '#': ignore = True
          elif c == '\n':
            if ignore: ignore = False
            else:
              var_name = name.getvalue().strip()
              if var_name in got: raise DotEnvTracedError("%s already declared." %var_name, 1, line, char)

              var_value = value.getvalue()
              got[var_name] = (Variable(var_name, var_value, VariableType.ENVIRONMENT), line, char-len(var_value))

            line += 1
            char = 0
            reading_value = False
            self.clear_strios(name, value)

          else:
            if ignore: continue
            elif c == '=': reading_value = True
            elif not reading_value: name.write(c)
            else: value.write(c)

    # Iterate over vars and parse their values.
    for gvar in got:
      var, line, start_char = got[gvar]
      value = str(var.value).strip()

      # Checking if the value is a string via "" or ''.
      if match(r"^\".*\"$", value): value = (str(value).strip()[1:-1], True)  # "" allows for ${}...
      elif match(r"^'.*'$", value): value = (str(value).strip()[1:-1], False)  # ...'' doesn't.

      # Checking if the value is an integer or a float.
      elif value.isnumeric(): value = int(value)
      elif self.isfloat(value): value = float(value)

      # Checking if the value is a boolean.
      elif value == "true" or value == "false": value = bool(value)

      # Just make it a string.
      else: value = (str(value), False)

      # (str, bool) -> value, whether the string supports ${}, which means it must use "".
      if isinstance(value, tuple):
        val, valid = value

        # Parse value (${}).
        if valid:
          tlvar = StringIO()
          dollar, lcurly = False, False

          for c in val:
            match c:
              case '$': dollar = True
              case '{' if dollar: lcurly, dollar = True, False

              case '}' if lcurly:
                tlval = tlvar.getvalue()
                if self.validate_var_name(tlval):
                  if tlval in got:
                    tlvobj = got[tlval][0]
                    val = val.replace("${%s}" %tlval, str(tlvobj.value))
                    lcurly, dollar = False, False

                  else: raise DotEnvError(f"{tlval} not declared (line {line}).", 1)
                else: raise DotEnvError(f"{tlval} is invalid (line {line}).", 1)

              case _ if lcurly:
                dollar = False
                tlvar.write(c)

              case _: dollar = False

        value = val
      var.value = value
      pairs[var.name] = var

    return pairs

  # I love regex!!
  def validate_var_name(self, _var_name: str) -> bool: return bool(match(r"^[a-zA-z_][a-zA-Z0-9_]*$", _var_name))

  def clear_strios(self, *strios: StringIO) -> None:
    for strio in strios:
      strio.seek(0)
      strio.truncate(0)

  def isfloat(self, _str: str) -> bool:
    if _str[0] == '.' or _str[-1] == '.': return False

    for c in _str:
      if not c.isnumeric() and not c == '.': return False

    return True
