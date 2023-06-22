from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runner import Runner
from os import getenv, scandir
from sys import exit


class Interpreter:
    def __init__(self, _flags: Flags) -> None:
        self.PWD = getenv("PWD")
        self.FLAGS = _flags
        self.lexer = Lexer(_flags)
        self.parser = Parser(_flags)
        self.runner = Runner(_flags)

    def interpret(self):
        bdpath = "%s/builddoc" %self.PWD if "builddoc" in [f.name.lower() for f in scandir(self.PWD)] else None
        if bdpath is None: exit(1)  # This shouldn't ever happen since this case is handled before this code is run.

        with open(bdpath, 'r') as builddoc:
            code = builddoc.read()
            self.parser.parse_tokens(self.lexer.tokenize(code))
