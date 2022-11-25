from interpreter.lexer import Lexer
from interpreter.parser import Parser
from out import BuildDocError

class Runner:
    """ Responsible for running the program, calling the lexer & parser. """

    @staticmethod
    def run_task(code: list[str], task: str | None, flags: dict[str, bool]) -> None:
        # FLAGS #
        always_zero: bool
        try: always_zero = flags["always_zero"]
        except KeyError: always_zero = False

        no_echo: bool
        try: no_echo = flags["no_echo"]
        except KeyError: no_echo = False

        verbose: bool
        try: verbose = flags["verbose"]
        except KeyError: verbose = False

        if len(code) < 1: raise BuildDocError("empty builddoc", 0 if always_zero else 1)

        dicts = Parser(always_zero, verbose).map(Lexer.tokenize(code, verbose, 0 if always_zero else 1)[1:])
        vars_map, cmds_map = dicts

        if task is None: task = [t for t in dicts[1]][0]
        cmds_map = cmds_map[task]
        commands, private = cmds_map

        if private: raise BuildDocError(f"cannot run private task '{task}'", 0 if always_zero else 1)
        elif len(commands) < 1: raise BuildDocError(f"task '{task}' has nothing to do", 0 if always_zero else 1)
        else: ...
