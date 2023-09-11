from interpreter.command import Command
from interpreter.macro import Macro
from interpreter.variable import Variable


class AST:
    """
    Abstract Syntax Tree. Keeps track of variables, tasks, etc.
    """

    def __init__(self) -> None:
        self.VARIABLES: dict[str, Variable] = {}
        self.TASKS: dict[str, list[Command | Macro]] = {}
