from os import environ, popen
from out import BuildDocTracedError


class Variable:
    def __init__(self, var_name: str, line: int, char: int, status_code: int) -> None:
        self.var_name, self.line, self.char, self.status_code, self.name = var_name, line+1, char, status_code, "VARIABLE"

    def value(self, vars_map: dict[str, tuple[str, bool]]) -> tuple[str, bool]:
        if self.var_name in vars_map: return vars_map[self.var_name]
        elif len(self.var_name) < 1: raise BuildDocTracedError("expected variable name", self.status_code, self.line, self.char)
        else: raise BuildDocTracedError("'%s' is undefined" %self.var_name, self.status_code, self.line+1, self.char)


class EnvVariable(Variable):
    def __init__(self, var_name: str, line: int, char: int, status_code: int) -> None:
        self.var_name, self.line, self.char, self.status_code, self.name = var_name, line+1, char, status_code, "ENV_VARIABLE"

    def value(self): return environ[self.var_name] if self.var_name in environ else ''


class ShellVariable(Variable):
    def __init__(self, cmd: str, line: int, char: int, status_code: int) -> None:
        self.cmd, self.line, self.char, self.status_code, self.name = cmd, line+1, char, status_code, "SHELL_VARIABLE"

    def value(self): return popen(self.cmd).read()
