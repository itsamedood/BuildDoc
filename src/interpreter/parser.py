from interpreter.tokens import *
from out import BuildDocTracedError


class Parser:
    """ Parses the tokens from the lexer. """

    status_code: int

    def __init__(self, always_zero: bool) -> None: self.status_code = 1 if not always_zero else 0

    def raise_unexpected_token(self, token: Token | LetterToken | NumberToken | UnknownToken, line: int, char: int):
        value = "whitespace" if token.value == ' ' else "'\\n'" if token.value == '\n' else "tab" if token.value == '\t' else f"'{token.value}'"
        raise BuildDocTracedError(f"unexpected {value}", self.status_code, line, char)

    def map(self, tokens: list[Token | LetterToken | NumberToken | UnknownToken]):
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

        # Iterate over every token.
        for t in range(len(tokens)):
            char += 1
            token = tokens[t]
            astr_open = dstr_open or sstr_open

            # Ignores comments until the line ends.
            if reading_comment and token is not Token.NEWLINE: continue

            # Reading section name.
            elif bracket_open and token is not Token.R_BRACK:
                if token is Token.PERIOD and not len(section) < 1: self.raise_unexpected_token(token, line, char)
                elif type(token) is LetterToken: section += token.value
                else: self.raise_unexpected_token(token, line, char)

            else:
                reading_comment = False

                if reading_var_value: print(token.value)
                else:
                    match token:
                        # PAIRS #
                        case Token.L_PAREN as t: ...
                        case Token.R_PAREN as t: ...
                        case Token.L_BRACE as t: ...
                        case Token.R_BRACE as t: ...

                        case Token.L_BRACK as t:
                            if not bracket_open: bracket_open = True
                            else: self.raise_unexpected_token(t, line, char)

                        case Token.R_BRACK as t:
                            if bracket_open: bracket_open = False
                            else: self.raise_unexpected_token(t, line, char)

                            if len(section) < 1: raise BuildDocTracedError("empty section declaration", self.status_code, line, char)
                            current_section, section = section, ''
                            task_map[current_section] = []

                        case Token.L_ANG_BRACK as t: ...
                        case Token.R_ANG_BRACK as t: ...

                        # OPERATORS #
                        case Token.DOLLAR as t: ...
                        case Token.AT as t: ...
                        case Token.QUESTION as t: ...
                        case Token.AMPERSAND as t: ...
                        case Token.PERCENT as t: ...
                        case Token.EQUAL as t: ...

                        # SYMBOLS #
                        case Token.HASH: reading_comment = True

                        case Token.D_QUOTE as t: ...
                        case Token.S_QUOTE as t: ...
                        case Token.BACKTICK as t: ...

                        case Token.PERIOD as t: ...
                        case Token.COMMA as t: ...
                        case Token.DASH as t: ...
                        case Token.UNDERSCORE as t: ...
                        case Token.PIPELINE as t: ...

                        # SPECIAL #
                        case Token.WHITESPACE as t:
                            if char <= 1: self.raise_unexpected_token(t, line, char)

                        case Token.BACKSLASH as t: ...

                        case Token.TAB as t:
                            if char <= 1: self.raise_unexpected_token(t, line, char)

                        case Token.NEWLINE as t:
                            line += 1
                            char = 0

                        case Token.EOF as t:
                            if bracket_open: raise BuildDocTracedError("unclosed '['", self.status_code, line, char)

                        # OTHER #
                        case t if type(t) is LetterToken:
                            if bracket_open: section += t.value
                            else: ...

                        case t if type(t) is NumberToken: ...  # Doubt this'll do much.
                        case t if type(t) is UnknownToken: ...
                        case _: ...

        # print(vars_map)
        print(task_map)
        return (vars_map, task_map)
