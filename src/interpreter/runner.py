from interpreter.flags import Flags
from interpreter.lexer import Lexer
from interpreter.macro import Macro
from interpreter.parser import Parser
from os import system
from out import BuildDocDebugMessage, BuildDocError
from typing import Any

class Runner:
    """ Responsible for running the program, calling the lexer & parser. """

    @staticmethod
    def abort(command: str, status: int): raise BuildDocError("'%s' exited with code %i." %(command, status), status)

    @staticmethod
    def interpret(code: list[str], task: str | None, flags: Flags) -> None:
        if len(code) < 1: raise BuildDocError("empty builddoc.", 0 if flags.always_zero else 1)

        dicts = Parser(flags).map(Lexer.tokenize(code, flags)[1:])
        vars_map, task_map = dicts

        if task is None: task = [t for t in dicts[1]][0]
        cmds_map = task_map[task]
        commands, private = cmds_map

        if private: raise BuildDocError("cannot run private task '%s'." %task, 0 if flags.always_zero else 1)
        elif len(commands) < 1: raise BuildDocError("task '%s' has nothing to do." %task, 0 if flags.always_zero else 1)
        else: Runner.run_task(task, vars_map, task_map, flags)

    @staticmethod
    def run_task(task: str, vars_map: dict[str, tuple[str, bool]], task_map: dict[str, tuple[list[tuple[str | Macro, int]], bool]], flags: Flags) -> None:
        if flags.verbose: BuildDocDebugMessage("EXECUTING TASK: %s" %task)

        cmds, private = task_map[task]
        conditional_commands: list[str | Macro] = []
        in_conditional, is_true, any_was_true, else_hit = False, False, False, False

        for tup in cmds:
            cmd, line = tup

            if in_conditional:
                match cmd:
                    case cmd if type(cmd) is str and cmd[:2] == "if": raise BuildDocError("nested if-statements are not allowed.", 1)
                    case cmd if type(cmd) is str and cmd[:4] == "elif":
                        condition = Parser.validate_conditional_syntax(cmd, flags.always_zero)

                        if condition is not None:
                            if is_true: is_true = False
                            else:
                                if flags.verbose: BuildDocDebugMessage("ELIF %s" %Parser.parse_string(condition, line-1, vars_map, flags))
                                is_true = Parser.evaluate_condition(Parser.parse_string(condition, line-1, vars_map, flags), 0 if flags.always_zero else 1, flags.verbose)

                    case cmd if type(cmd) is str and cmd[:4] == "else":
                        if flags.verbose: BuildDocDebugMessage("ELSE")
                        if is_true: is_true = False
                        if not any_was_true: else_hit = True

                    case "endif":
                        if flags.verbose: BuildDocDebugMessage("ENDIF")
                        if flags.verbose: BuildDocDebugMessage("Conditional commands gathered: %s" %conditional_commands)

                        for cmd in conditional_commands:
                            if type(cmd) is str:
                                c = Parser.parse_string(cmd, line-1, vars_map, flags)
                                if flags.verbose:
                                    BuildDocDebugMessage("CMD: %s" %c)
                                    status = 0

                                if c[0] == '&': status = system(c[1:])
                                else: print(c); status = system(c)

                                if status > 0: Runner.abort(cmd, status)

                            elif type(cmd) is Macro: Runner.run_macro(cmd, vars_map, task_map, flags)

                        in_conditional = False

                    case cmd:
                        # Check if condition is valid. If it is, append the command to conditional_commands.
                        if is_true or (else_hit and not any_was_true): conditional_commands.append(cmd)

                if is_true: any_was_true = True

            elif type(cmd) is str:
                    if cmd.strip()[:2] == "if":
                        condition = Parser.validate_conditional_syntax(cmd, flags.always_zero)

                        if condition is not None:
                            if flags.verbose: BuildDocDebugMessage("IF %s" %Parser.parse_string(condition, line-1, vars_map, flags))
                            is_true = Parser.evaluate_condition(Parser.parse_string(condition, line-1, vars_map, flags), 0 if flags.always_zero else 1, flags.verbose)
                            in_conditional = True

                    else:
                        c = Parser.parse_string(cmd, line-1, vars_map, flags)
                        if c[0] == '&': status = system(c[1:])
                        else: print(c); status = system(c)
                        if flags.verbose: BuildDocDebugMessage("CMD: %s" %cmd)
                        if flags.verbose: status = 0

                        if status > 0: Runner.abort(cmd, status)

            elif type(cmd) is Macro: Runner.run_macro(cmd, vars_map, task_map, flags)

    @staticmethod
    def run_macro(cmd: Macro, vars_map: dict[str, tuple[str, bool]], task_map: dict[str, tuple[list[tuple[str | Macro, int]], bool]], flags: Flags):
        match cmd.macro_name:
            case "goto":
                if len(cmd.args) == 1: Runner.run_task(cmd.args[0], vars_map, task_map, flags)

            case _: cmd.call()
