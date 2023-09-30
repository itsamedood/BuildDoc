from interpreter.variable import *
from interpreter.ast import AST
from interpreter.flags import Flags
from interpreter.tokens import Token
from out import BuildDocTracedError, BuildDocDebugMessage, get_line


class Parser:
    def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

    def parse_tokens(self, _tokens: list[tuple[Token, str | int | None]]) -> AST:
        TREE = AST()

        # General variables.
        task, current_task = '', ''
        ignore, bracket_open = False, False
        line, char = 1, 0

        # Variable related variables.
        reading_vars, reading_var_name = False, False
        d_quote, s_quote = False, False
        var_name, var_value = '', ''

        for i, t in enumerate(_tokens):
            token, value = t
            char += 1

            if token is Token.NEWLINE:
                if ignore: ignore = False

            if token is Token.HASH: ignore = True
            if ignore: continue

            if bracket_open and token is not Token.R_BRACKET:
                if token is not Token.LETTER: self.raise_unexpected(str(value), line, char, get_line())
                else: task += str(value)

            if reading_vars:
                if reading_var_name:
                    if token is Token.LETTER: var_name += str(value)
                    elif token is Token.EQUAL: reading_var_name = False
                    else: self.raise_unexpected(str(value), line, char, get_line())

                else:
                    if token is Token.D_QUOTE: d_quote = not d_quote
                    # if token is Token.S_QUOTE and not d_quote: s_quote = not s_quote

                    if d_quote or s_quote:
                        if token is not Token.D_QUOTE: var_value += str(value)

                    if not d_quote:
                        BuildDocDebugMessage(f"{var_name} = {var_value}", self.FLAGS.verbose)
                        TREE.VARIABLES[var_name] = Variable(var_name, var_value, VariableType.REGULAR)
                        reading_vars = False

                continue

            match token:
                case Token.LETTER:
                    if len(current_task) < 1 and not bracket_open:
                        reading_vars, reading_var_name = True, True
                        var_name += str(value)

                case Token.NUMBER: ...

                # Brackets #
                case Token.L_PAREN: ...
                case Token.R_PAREN: ...
                case Token.L_BRACE: ...
                case Token.R_BRACE: ...

                case Token.L_BRACKET:
                    if bracket_open: self.raise_unexpected('[', line, char, get_line())
                    else: bracket_open, reading_vars = True, False

                case Token.R_BRACKET:
                    if not bracket_open: self.raise_unexpected(']', line, char, get_line())
                    else: bracket_open = False

                    current_task, task = task, ''
                    TREE.TASKS[current_task] = []
                    BuildDocDebugMessage("Current task: %s" %current_task, self.FLAGS.verbose)

                case Token.L_ANGLE_BRACKET: ...
                case Token.R_ANGLE_BRACKET: ...

                # Operators #
                case Token.DOLLAR: ...
                case Token.AT: ...
                case Token.QUESTION_MARK: ...
                case Token.AMPERSAND: ...
                case Token.PERCENT: ...
                case Token.EQUAL: ...

                # Symbols #
                case Token.HASH: ignore = True

                case Token.D_QUOTE: ...
                case Token.S_QUOTE: ...
                case Token.BACKTICK: ...
                case Token.PERIOD: ...
                case Token.COMMA: ...
                case Token.HYPHEN: ...
                case Token.UNDERSCORE: ...
                case Token.PIPELINE: ...
                case Token.EXCLAMATION: ...
                case Token.COLON: ...
                case Token.SEMICOLON: ...
                case Token.CAROT: ...
                case Token.ASTERISK: ...
                case Token.TILDE: ...
                case Token.FORWARD_SLASH: ...
                case Token.BACKWARD_SLASH: ...

                # Other #
                case Token.WHITESPACE: ...
                case Token.TAB: ...

                case Token.NEWLINE:
                    if ignore: ignore = False

                    line += 1
                    char = 0

                case Token.BROKEN_STR: ...
                case Token.UNKNOWN: ...
                case Token.EOF: ...

                # case token: print("how did this happen?")

        return TREE

    def raise_unexpected(self, _unexpected_char: str, _line: int, _char: int, _from_line: int | None = None) -> None:
        if self.FLAGS.debug and _from_line is not None: raise BuildDocTracedError(f"unexpected '{_unexpected_char}' @{_from_line}", 0 if self.FLAGS.debug else 1, _line, _char)
        else: raise BuildDocTracedError("unexpected %s" %_unexpected_char, 0 if self.FLAGS.debug else 1, _line, _char)
