from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from os import system
from out import BuildDocError, BuildDocNote

class Runner:
    """ Responsible for running the program, calling the lexer & parser. """

    @staticmethod
    def abort(command: str, status: int): raise BuildDocError("'%s' exited with code %i" %(command, status), status)

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
        else:
            if flags.verbose: BuildDocNote("EXECUTING...")

            for tup in commands:
                command, line = tup
                c = Parser.parse_string(command, line, vars_map, flags)
                status = system(c)

                if status > 0: Runner.abort(command, status)
