from interpreter.tokens import *
from out import BuildDocTracedError


class Parser:
    """ Parses the tokens from the lexer. """

    status_code: int

    def __init__(self, always_zero: bool) -> None: self.status_code = 1 if not always_zero else 0

    def raise_unexpected_token(self, token: Token | LetterToken | NumberToken | UnknownToken | StringToken, line: int, char: int):
        value = "whitespace" if token.value == ' ' else "'\\n'" if token.value == '\n' else "tab" if token.value == '\t' else f"'{token.value}'"
        raise BuildDocTracedError(f"unexpected {value}", self.status_code, line, char)

    def map(self, tokens: list[Token | LetterToken | NumberToken | UnknownToken | StringToken]):
        """ Maps variables with their values, and tasks with their commands. """

        # Parser vars.
        line, char = 1, 0
        var_name, var_value = '', ''
        section, current_section = '', ''
        command, var = '', ''
        parenth_open, bracket_open, brace_open = False, False, False
        dstr_open, sstr_open, astr_open = False, False, False
        backslash = False
        reading_comment, reading_var_value = False, False

        # Dicts.
        vars_map: dict[str, str] = {}
        task_map: dict[str, list[str]] = {}

        # Ensuring line 1 doesn't start with a whitespace or tab.
        if tokens[0] is Token.WHITESPACE or tokens[0] is Token.TAB: self.raise_unexpected_token(tokens[0], 1, 1)

        # Iterate over every token.
        for t in range(len(tokens)):
            char += 1
            token = tokens[t]
            astr_open = dstr_open or sstr_open

            # Ignores comments until the line ends.
            if reading_comment and token is not Token.NEWLINE: continue

            # Reading section name.
            elif bracket_open and token is not Token.R_BRACK:
                if token is Token.PERIOD and len(section) < 1: section += token.value
                elif type(token) is LetterToken: section += token.value
                else: self.raise_unexpected_token(token, line, char)

            else:
                reading_comment = False

                if reading_var_value: print(token.value)
                else:
                    match token:
                        # PAIRS #
                        case Token.L_PAREN as tok: ...
                        case Token.R_PAREN as tok: ...
                        case Token.L_BRACE as tok: ...
                        case Token.R_BRACE as tok: ...

                        case Token.L_BRACK as tok:
                            if not bracket_open: bracket_open = True
                            else: self.raise_unexpected_token(tok, line, char)

                        case Token.R_BRACK as tok:
                            if bracket_open: bracket_open = False
                            else: self.raise_unexpected_token(tok, line, char)

                            if len(section) < 1: raise BuildDocTracedError("empty section declaration", self.status_code, line, char)
                            current_section, section = section, ''
                            task_map[current_section] = []

                        case Token.L_ANG_BRACK as tok: ...
                        case Token.R_ANG_BRACK as tok: ...

                        # OPERATORS #
                        case Token.DOLLAR as tok: ...
                        case Token.AT as tok: ...
                        case Token.QUESTION as tok: ...
                        case Token.AMPERSAND as tok: ...
                        case Token.PERCENT as tok: ...
                        case Token.EQUAL as tok: ...

                        # SYMBOLS #
                        case Token.HASH: reading_comment = True

                        case Token.D_QUOTE as tok: ...
                        case Token.S_QUOTE as tok: ...
                        case Token.BACKTICK as tok: ...

                        case Token.PERIOD as tok: ...
                        case Token.COMMA as tok: ...
                        case Token.DASH as tok: ...
                        case Token.UNDERSCORE as tok: ...
                        case Token.PIPELINE as tok: ...

                        # SPECIAL #
                        case Token.WHITESPACE as tok:
                            if tokens[t-1] is Token.NEWLINE: self.raise_unexpected_token(tok, line, char)

                        case Token.BACKSLASH as tok: backslash = not backslash

                        case Token.TAB as tok:
                            if tokens[t-1] is Token.NEWLINE: self.raise_unexpected_token(tok, line, char)

                        case Token.NEWLINE as tok:
                            line += 1
                            char = 0

                        case Token.SOF as tok: ...

                        case Token.EOF as tok:
                            if bracket_open: raise BuildDocTracedError("unclosed '['", self.status_code, line, char)

                        # OTHER #
                        case t if type(t) is LetterToken:
                            if bracket_open: section += t.value
                            else: ...

                        case t if type(t) is NumberToken: ...  # Doubt this'll do much.
                        case t if type(t) is UnknownToken: ...
                        case t if type(t) is StringToken: ...
                        case _: ...

        # print(vars_map)
        print(task_map)
        return (vars_map, task_map)
