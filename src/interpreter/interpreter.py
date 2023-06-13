from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runner import Runner


class Interpreter:
    def __init__(self, _flags: Flags) -> None:
        self.FLAGS = _flags
        self.lexer = Lexer()
        self.parser = Parser()
        self.runner = Runner()

    def interpret(self): ...
