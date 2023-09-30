from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runner import Runner
from out import BuildDocDebugMessage
from os import getenv


class Interpreter:
    def __init__(self, _flags: Flags) -> None:
        self.PWD = getenv("PWD")
        self.FLAGS = _flags
        self.lexer = Lexer(_flags)
        self.parser = Parser(_flags)
        self.runner = Runner(_flags)

    def interpret(self, _path: str):
        with open(_path, 'r') as builddoc:
            code = builddoc.read()
            self.TREE = self.parser.parse_tokens(self.lexer.tokenize(code))
            BuildDocDebugMessage("TASKS: %s" %self.TREE.TASKS, self.FLAGS.verbose)
            BuildDocDebugMessage("VARIABLES: %s" %self.TREE.VARIABLES, self.FLAGS.verbose)
