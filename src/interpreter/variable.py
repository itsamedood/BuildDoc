from out import BuildDocTracedError


class Variable:
    vars_map: dict[str, tuple[str, bool]] = {}

    def __init__(self, var_name: str, line: int, char: int, status_code: int) -> None:
        self.var_name, self.line, self.char, self.status_code, self.name = var_name, line, char, status_code, "VARIABLE"

    def set_vars_map(self, _vars_map: dict[str, tuple[str, bool]]): self.vars_map = _vars_map

    @property
    def value(self) -> tuple[str, bool]:
        if self.var_name in self.vars_map: return self.vars_map[self.var_name]
        else: raise BuildDocTracedError(f"'{self.var_name}' is undefined", self.status_code, self.line+1, self.char)
