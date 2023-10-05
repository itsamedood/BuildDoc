from interpreter.variable import *
from dotenv.out import DotEnvTracedError
from io import StringIO
from os import getcwd, scandir


class DotEnv:
    @staticmethod
    def read() -> dict[str, Variable]:
        """ Reads all `.env` files in the current working directory. """

        pairs: dict[str, Variable] = {}
        dotenv_files = [e for e in scandir(getcwd()) if e.is_file() and e.name[-4:] == ".env"]

        name, value = StringIO(), StringIO()
        line, char = 1, 0
        ignore, reading_value = False, False

        for dotenv_file in dotenv_files:
            with open(dotenv_file.path, 'r') as dotenv:
                lines = dotenv.read()

                for i, c in enumerate(lines):
                    if c == '#': ignore = True
                    elif c == '\n':
                        if ignore: ignore = False
                        else:
                            var_name = name.getvalue().strip()
                            var_value = value.getvalue()

                            if var_value[0] == ' ': var_value = var_value[1:]

                            print(f"{var_name} = {var_value}")
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

        return pairs

    @staticmethod
    def clear_strios(*strios: StringIO) -> None:
        for strio in strios:
            strio.seek(0)
            strio.truncate(0)
