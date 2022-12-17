from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from out import BuildDocError

class Runner:
    """ Responsible for running the program, calling the lexer & parser. """

    @staticmethod
    def run_task(code: list[str], task: str | None, flags: Flags) -> None:
        if len(code) < 1: raise BuildDocError("empty builddoc", 0 if flags.always_zero else 1)

        dicts = Parser(flags).map(Lexer.tokenize(code, flags)[1:])
        vars_map, cmds_map = dicts

        if task is None: task = [t for t in dicts[1]][0]
        cmds_map = cmds_map[task]
        commands, private = cmds_map

        if private: raise BuildDocError("cannot run private task '%s'" %task, 0 if flags.always_zero else 1)
        elif len(commands) < 1: raise BuildDocError("task '%s' has nothing to do" %task, 0 if flags.always_zero else 1)
        else: ...
