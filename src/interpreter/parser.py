from interpreter.variable import *
from dotenv.dotenv import DotEnv
from interpreter.ast import AST
from interpreter.flags import Flags
from interpreter.tokens import Token
from io import StringIO
from out import BuildDocDebugMessage, BuildDocTracedError, clear_strios


class Parser:
    def __init__(self, _flags: Flags) -> None:
        self.FLAGS = _flags
        self.TREE = AST(_flags)
        self.line, self.char, = 1, 0

        # Read and parse all `.env` in cwd.
        self.TREE.VARIABLES |= DotEnv.read()

    def parse_tokens(self, _tokens: list[tuple[Token, str | int | None]]) -> AST:
        # General variables.
        task, current_task = StringIO(), ''
        ignore, bracket_open = False, False

        # Variable related variables.
        reading_vars, reading_var_name = False, False
        d_quote, s_quote = False, False
        var_name, var_value = StringIO(), StringIO()

        for i, t in enumerate(_tokens):
            token, value = t
            self.char += 1

            if token is Token.NEWLINE:
                if ignore: ignore = False

            if token is Token.HASH: ignore = True
            if ignore: continue

            if bracket_open and token is not Token.R_BRACKET:
                if token is not Token.LETTER and token is not Token.UNDERSCORE: self.raise_unexpected(str(value), self.line, self.char)
                else: task.write(str(value))

            if reading_vars:
                if reading_var_name:
                    if token is Token.LETTER or token is Token.UNDERSCORE: var_name.write(str(value))
                    elif token is Token.EQUAL: reading_var_name = False
                    else: self.raise_unexpected(str(value), self.line, self.char)

                else:
                    if token is Token.D_QUOTE: d_quote = not d_quote
                    # if token is Token.S_QUOTE and not d_quote: s_quote = not s_quote

                    if d_quote or s_quote:
                        if token is not Token.D_QUOTE: var_value.write(str(value))

                    if not d_quote:
                        BuildDocDebugMessage(f"{var_name.getvalue()} = {var_value.getvalue()}", _verbose=self.FLAGS.verbose)
                        if var_name in self.TREE.VARIABLES: raise BuildDocTracedError("var %s already declared" %var_name, 0 if self.FLAGS.debug else 1, self.line, self.char, self.FLAGS.debug)
                        else:
                            vv = var_value.getvalue()
                            vv = self.parse_text(vv)

                            self.TREE.VARIABLES[var_name.getvalue()] = Variable(var_name.getvalue(), var_value.getvalue(), VariableType.REGULAR)

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
                    if bracket_open: self.raise_unexpected('[', self.line, self.char)
                    else: bracket_open, reading_vars = True, False

                case Token.R_BRACKET:
                    if not bracket_open: self.raise_unexpected(']', self.line, self.char)
                    else: bracket_open = False

                    current_task = task.getvalue()
                    clear_strios(task)

                    self.TREE.TASKS[current_task] = []
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

                    self.line += 1
                    self.char = 0

                case Token.BROKEN_STR: ...
                case Token.UNKNOWN: ...
                case Token.EOF: ...

                # case token: print("how did this happen?")

        return self.TREE

    def parse_text(self, _text: str) -> str:
        """ Replaces variables of all types in `_text`. """

        var_name = StringIO()
        reading_var, reading_env_var = False, False

        for i, c in enumerate(_text):
            if c == Token.DOLLAR.value: reading_var = True; continue
            if c == Token.AT.value: reading_env_var = True; continue

            if reading_var:
                if i == len(_text)-1:
                    if c.isalpha() or c == Token.UNDERSCORE.value: var_name.write(c)
                    reading_var = False

                elif c.isalpha() or c == Token.UNDERSCORE.value:
                    var_name.write(c)
                    continue
                else:
                    reading_var = False
                    continue

            else:
                vn_val = var_name.getvalue()
                BuildDocDebugMessage("Got: %s" %vn_val, _verbose=self.FLAGS.verbose)

                if vn_val in self.TREE.VARIABLES:
                    _text = _text.replace('$%s' %vn_val, self.TREE.VARIABLES[vn_val].value)

        BuildDocDebugMessage(_text, _verbose=self.FLAGS.verbose)
        return _text

    def parse_var_values(self) -> None:
        for var_name in self.TREE.VARIABLES:
            var = self.TREE.VARIABLES[var_name]
            var.value = self.parse_text(var.value)
            BuildDocDebugMessage("After parse: %s" %var.value, _verbose=True)

    def raise_unexpected(self, _unexpected_char: str, _line: int, _char: int) -> None:
        """ Shortcut for raising a traced error for an unexpected character. """
        raise BuildDocTracedError("unexpected %s" %_unexpected_char, 1, _line, _char, self.FLAGS.debug)
