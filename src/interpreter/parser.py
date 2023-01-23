from interpreter.tokens import *
from interpreter.flags import Flags
from interpreter.macro import Macro
from interpreter.variable import Variable
from out import BuildDocError, BuildDocNote, BuildDocTracedError, BuildDocTracedWarning


class Parser:
    """ Parses the tokens from the lexer. """

    def __init__(self, flags: Flags) -> None:
        self.status_code, self.verbose = 1 if not flags.always_zero else 0, flags.verbose

    def raise_unexpected_token(self, token: Token | LetterToken | NumberToken | UnknownToken | StringToken | Variable | Macro, line: int, char: int):
        value = "whitespace" if token.value == ' ' else "newline" if token.value == '\n' else "tab" if token.value == '\t' else "'%s'" %token.value
        raise BuildDocTracedError("unexpected %s" %value, self.status_code, line, char)

    # Currently just replaces regular variables in the string.
    @staticmethod
    def parse_string(string:str, line: int, vars_map: dict[str, tuple[str, bool]], flags: Flags) -> str:
        parsed_string = string

        def throw(char: str, c: int):
            value = "whitespace" if char == ' ' else "newline" if char == '\n' else "tab" if char == '\t' else "'%s'" %char
            raise BuildDocTracedError("unexpected %s" %value, 0 if flags.always_zero else 1, line, c+1)

        reading_var = False
        var = ''
        reg_vars: list[Variable] = []

        for c in range(len(string)):
            char = string[c]

            if reading_var:
                if char.lower() in Token.LETTER.value or char == Token.UNDERSCORE.value: var += char
                elif char == Token.NEWLINE.value: throw(char, c)
                else:
                    reg_vars.append(Variable(var, line, c, 0 if flags.always_zero else 1))
                    var, reading_var = '', False

            match char:
                case Token.DOLLAR.value: reading_var = True

                case Token.WHITESPACE.value: ...
                case l: ...

            if c == len(string)-1: reg_vars.append(Variable(var, line, c, 0 if flags.always_zero else 1))
        if flags.verbose: BuildDocNote(f"REG VARS FOUND: {[rv.var_name for rv in reg_vars]}")

        for v in range(len(reg_vars)):
            var = reg_vars[v]
            value, constant = var.value(vars_map)
            parsed_string = parsed_string.replace("$%s" %var.var_name, value)

        return parsed_string

    def map(self, tokens: list[Token | LetterToken | NumberToken | UnknownToken | StringToken | Variable]):
        """ Maps variables with their values, and tasks with their commands. """

        # Parser vars.
        line, char = 1, 0
        var_name, var_value = '', ''
        section, current_section = '', ''
        command = ''
        parenth_open, bracket_open, brace_open = False, False, False
        dstr_open, sstr_open, astr_open = False, False, False
        backslash = False
        reading_comment, reading_var_value = False, False

        # Dicts.
        vars_map: dict[str, tuple[str, bool]] = {}
        task_map: dict[str, tuple[list[tuple[str, int]], bool]] = {}

        # Ensuring line 1 doesn't start with a whitespace or tab.
        if tokens[0] is Token.WHITESPACE or tokens[0] is Token.TAB: self.raise_unexpected_token(tokens[0], 1, 1)

        # Iterate over every token.
        for t in range(len(tokens)):
            if self.verbose: BuildDocNote(f"Current line: {line}")
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

                if not bracket_open and len(current_section) < 1 and not reading_var_value and token is not Token.EQUAL and token is not Token.L_BRACK:
                    if type(token) is LetterToken or token is Token.UNDERSCORE: var_name += token.value
                    elif token is Token.PERIOD and len(var_name) < 1: var_name += token.value
                    elif type(token) is Variable: var_name += token.value(vars_map)[0]

                else:
                    if len(current_section) > 0 and token is not Token.NEWLINE and token is not Token.L_BRACK and token is not Token.R_BRACK and token is not Token.HASH:
                        if type(token.value) is str: command += token.value
                        elif type(token) is Variable: command += token.value(vars_map)[0]

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
                            private = False

                            if current_section[0] == Token.PERIOD.value:
                                private = True
                                current_section = current_section[1:]

                            if current_section in task_map: raise BuildDocError("duplicate task: '%s'" %current_section, self.status_code)

                            task_map[current_section] = ([], private)

                        case Token.L_ANG_BRACK as tok: ...
                        case Token.R_ANG_BRACK as tok: ...

                        # OPERATORS #
                        case Token.DOLLAR as tok: ...
                        case Token.AT as tok: ...
                        case Token.QUESTION as tok: ...
                        case Token.AMPERSAND as tok: ...
                        case Token.PERCENT as tok: ...
                        case Token.EQUAL as tok:
                            if len(var_name) < 1 and var_name[0] == Token.PERIOD.value: self.raise_unexpected_token(tok, line, char)

                            if tokens[t+1] is Token.BROKEN_STR: raise BuildDocTracedError("unclosed string", self.status_code, line, char)
                            elif type(tokens[t+1]) is not StringToken: raise BuildDocTracedError("value must be in quotes", self.status_code, line, char)

                            reading_var_value = True

                        # SYMBOLS #
                        case Token.HASH: reading_comment = True
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
                            if reading_var_value:
                                if type(tokens[t-1]) is not StringToken: raise BuildDocTracedError("expected value", self.status_code, line, char)

                            cmd = command.strip()  # Close your eyes, the command is stripping!
                            if len(cmd) > 0:
                                if self.verbose: print("COMMAND = %s" %cmd)
                                task_map[current_section][0].append((cmd, line+3))
                                command = ''

                            var_name, var_value = '', ''
                            reading_var_value = False
                            line += 1
                            char = 0

                        case Token.BROKEN_STR: raise BuildDocTracedError("unclosed string", self.status_code, line, char)

                        case Token.SOF as tok: ...

                        case Token.EOF as tok:
                            if bracket_open: raise BuildDocTracedError("unclosed '['", self.status_code, line, char)
                            if astr_open: raise BuildDocTracedError("unclosed string", self.status_code, line, char)

                        # OTHER #
                        case tok if type(tok) is Variable:
                            value, constant = tok.value(vars_map)

                            if self.verbose: print("value: %s" %value)
                            if self.verbose: print("constant: %s" %("yes" if constant else "no"))

                        case tok if type(tok) is LetterToken:
                            if bracket_open: section += tok.value
                            elif not bracket_open and len(current_section) < 1 and not reading_var_value: var_name += tok.value
                            else: ...

                        case t if type(t) is NumberToken: ...  # Doubt this'll do much.
                        case t if type(t) is UnknownToken: ...

                        case t if type(t) is StringToken:
                            if reading_var_value: var_value = t.value
                            reading_var_value = False

                            if len(current_section) < 1:
                                if len(var_value) < 1: BuildDocTracedWarning("'%s' has empty value" %var_name, line, char)
                                if var_name[0] == Token.PERIOD.value: vars_map[var_name[1:]] = (var_value, True)
                                else: vars_map[var_name] = (var_value, False)

                                var_name, var_value = '', ''

                        case _: ...

        if self.verbose: print("VARS MAP:", vars_map)
        if self.verbose: print("TASK MAP:", task_map)
        return (vars_map, task_map)
