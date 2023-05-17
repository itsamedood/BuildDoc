from ansi import Ansi
from interpreter.flags import Flags
from out import BuildDocMacroError, BuildDocMacroArgumentError, BuildDocError, BuildDocWarning
from typing import Any


class Macro:
    name = "MACRO"
    value = "macro"

    def __init__(self, macro_name: str, args: list[str], line: int, flags: Flags, vars_map: dict[str, tuple[str, bool]] | None, cmds_map: tuple[list[tuple[str | Any, int]], bool] | None) -> None:
        self.macro_name = macro_name
        self.args = args
        self.line = line
        self.flags = flags
        self.status_code = 0 if flags.always_zero else 1
        self.vars_map, self.cmds_map = vars_map, cmds_map

    # exa = "Expected `x` Arguments".
    def raise_exa(self, expected: int): raise BuildDocMacroArgumentError(self.macro_name, expected, len(self.args), self.status_code)

    def call(self) -> None:
        match self.macro_name:
            case "error":
                if len(self.args) < 2 or len(self.args) > 2: self.raise_exa(2)
                raise BuildDocError(f"({Ansi.style.LIGHT}line {self.line+1}{Ansi.special.RESET}): {self.args[0]}", int(self.args[1].strip()))

            case "warn":
                if len(self.args) < 1 or len(self.args) > 1: self.raise_exa(1)
                BuildDocWarning(self.args[0])

            case macro_name: BuildDocMacroError(self.macro_name, "unknown macro", self.status_code)
