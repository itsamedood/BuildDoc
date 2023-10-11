from interpreter.variable import *
from bdotenv.out import DotEnvTracedError
from io import StringIO
from re import match
from os import getcwd, scandir


class DotEnv:
    @staticmethod
    def read() -> dict[str, Variable]:
        """ Reads all `.env` files in the current working directory. """

        pairs: dict[str, Variable] = {}
        got: dict[str, tuple[Variable, int, int]] = {}  # Var, line, char value started at.
        dotenv_files = [e for e in scandir(getcwd()) if e.is_file() and e.name[-4:] == ".env"]

        name, value = StringIO(), StringIO()
        line, char = 1, 0
        ignore, reading_value = False, False

        for dotenv_file in dotenv_files:
            with open(dotenv_file.path, 'r') as dotenv:
                lines = dotenv.read()

                # Read through and just get vars and their values.
                for i, c in enumerate(lines):
                    char += 1
                    if c == '#': ignore = True
                    elif c == '\n':
                        if ignore: ignore = False
                        else:
                            var_name = name.getvalue().strip()

                            if ' ' in [c for c in var_name if c == ' ']: raise DotEnvTracedError("spaces not allowed in variable name.", 1, line, char)
                            if var_name in got: raise DotEnvTracedError("%s already declared." %var_name, 1, line, char)

                            var_value = value.getvalue()
                            got[var_name] = (Variable(var_name, var_value, VariableType.ENVIRONMENT), line, char-len(var_value))

                        line += 1
                        char = 0
                        reading_value = False
                        DotEnv.clear_strios(name, value)

                    else:
                        if ignore: continue
                        if c == '=': reading_value = True

                        elif not reading_value:
                            if c.isdigit() and len(name.getvalue()) < 1: raise DotEnvTracedError("var name cannot start with a digit.", 1, line, char)
                            name.write(c)

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
            elif DotEnv.isfloat(value): value = float(value)

            # Checking if the value is a boolean.
            elif value == "true" or value == "false": value = bool(value)

            # Just make it a string.
            else: value = (str(value), False)

            # (str, bool) -> value, whether the string supports ${}, which means it must use "".
            if isinstance(value, tuple):
                val, valid = value
                # print(f"{val} {type(val)} is {valid} @{line}:{char}")

                if valid: ...  # Parse value (${}).
                value = val

            # int, float, or bool.
            else: ...

            var.value = value
            pairs[var.name] = var

        return pairs

    @staticmethod
    def clear_strios(*strios: StringIO) -> None:
        for strio in strios:
            strio.seek(0)
            strio.truncate(0)

    @staticmethod
    def isfloat(_str: str) -> bool:
        if _str[0] == '.' or _str[-1] == '.': return False

        for c in _str:
            if not c.isnumeric() and not c == '.': return False

        return True