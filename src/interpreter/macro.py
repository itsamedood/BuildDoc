from out import BuildDocTracedError


class Macro:
    name = "MACRO"
    value = "macro"

    def __init__(self, macro_name: str, args: list[str]) -> None: self.macro_name, self.args = macro_name, args

    def call(self) -> ...: ...
