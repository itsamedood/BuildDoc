from dotenv import load_dotenv
from interpreter.flags import Flags
from interpreter.interpreter import Interpreter
from out import Ansi


class Cli:
    def __init__(self, argv: list[str]) -> None:
        self.FLAGS = Flags([a[1:] for a in argv if a[0] == '-' and len(a) > 1])
        self.ARGS = [a for a in argv if not a[0] == '-']
        self.ARGS.pop()

    def process_args(self):
        task = None
        if len(self.ARGS) > 0: task = self.ARGS[0]

        intrptr = Interpreter(self.FLAGS)
        intrptr.interpret()
