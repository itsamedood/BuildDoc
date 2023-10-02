from interpreter.variable import *
from interpreter.ast import AST
from interpreter.flags import Flags
from interpreter.tokens import Token
from io import StringIO
from out import BuildDocDebugMessage, BuildDocTracedError, clear_strios


class Parser:
    def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

    def parse_tokens(self, _tokens: list[tuple[Token, str | int | None]]) -> AST:
        TREE = AST(self.FLAGS)

        # General variables.
        task, current_task = StringIO(), ''
        ignore, bracket_open = False, False
        line, char = 1, 0

        # Variable related variables.
        reading_vars, reading_var_name = False, False
        d_quote, s_quote = False, False
        var_name, var_value = StringIO(), StringIO()

        for i, t in enumerate(_tokens):
            token, value = t
            char += 1

            if token is Token.NEWLINE:
                if ignore: ignore = False

            if token is Token.HASH: ignore = True
            if ignore: continue

            if bracket_open and token is not Token.R_BRACKET:
                if token is not Token.LETTER and token is not Token.UNDERSCORE: self.raise_unexpected(str(value), line, char)
                else: task.write(str(value))

            if reading_vars:
                if reading_var_name:
                    if token is Token.LETTER or token is Token.UNDERSCORE: var_name.write(str(value))
                    elif token is Token.EQUAL: reading_var_name = False
                    else: self.raise_unexpected(str(value), line, char)

                else:
                    if token is Token.D_QUOTE: d_quote = not d_quote
                    # if token is Token.S_QUOTE and not d_quote: s_quote = not s_quote

                    if d_quote or s_quote:
                        if token is not Token.D_QUOTE: var_value.write(str(value))

                    if not d_quote:
                        BuildDocDebugMessage(f"{var_name.getvalue()} = {var_value.getvalue()}", _verbose=self.FLAGS.verbose)
                        if var_name in TREE.VARIABLES: raise BuildDocTracedError("var %s already declared" %var_name, 0 if self.FLAGS.debug else 1, line, char, self.FLAGS.debug)
                        else: TREE.VARIABLES[var_name.getvalue()] = Variable(var_name.getvalue(), var_value.getvalue(), VariableType.REGULAR)

                        clear_strios(var_name, var_value)
                        reading_vars = False

                continue

            if len(current_task) > 0:
                if token is Token.L_BRACKET: ...
                elif token is Token.NEWLINE: ...
                else: ...

            match token:
                case Token.LETTER:
                    if len(current_task) < 1 and not bracket_open:
                        reading_vars, reading_var_name = True, True
                        var_name.write(str(value))

                case Token.NUMBER: ...

                # Brackets #
                case Token.L_PAREN: ...
                case Token.R_PAREN: ...
                case Token.L_BRACE: ...
                case Token.R_BRACE: ...

                case Token.L_BRACKET:
                    if bracket_open: self.raise_unexpected('[', line, char)
                    else: bracket_open, reading_vars = True, False

                case Token.R_BRACKET:
                    if not bracket_open: self.raise_unexpected(']', line, char)
                    else: bracket_open = False

                    current_task = task.getvalue()
                    clear_strios(task)

                    TREE.TASKS[current_task] = []
                    BuildDocDebugMessage("Current task: %s" %current_task, _verbose=self.FLAGS.verbose)

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

    def parse_text(self, _text: str) -> str:
        """ Replaces variables of all types in `_text`. """

        for i, c in enumerate(_text): BuildDocDebugMessage(c, _verbose=self.FLAGS.verbose)

        return _text

    def raise_unexpected(self, _unexpected_char: str, _line: int, _char: int) -> None:
        """ Shortcut for raising a traced error for an unexpected character. """
        raise BuildDocTracedError("unexpected %s" %_unexpected_char, 0 if self.FLAGS.debug else 1, _line, _char, self.FLAGS.debug)
