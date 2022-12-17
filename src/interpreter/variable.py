from out import BuildDocTracedError


class Variable:
    def __init__(self, var_name: str, line: int, char: int, status_code: int) -> None:
        self.var_name, self.line, self.char, self.status_code, self.name = var_name, line, char, status_code, "VARIABLE"

    def value(self, vars_map: dict[str, tuple[str, bool]]) -> tuple[str, bool]:
        if self.var_name in vars_map: return vars_map[self.var_name]
        else: raise BuildDocTracedError("'%s' is undefined" %self.var_name, self.status_code, self.line+1, self.char)
