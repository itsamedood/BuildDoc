from enum import Enum
from interpreter.tokens import *
from interpreter.variable import *
from interpreter.flags import Flags
from interpreter.macro import Macro
from out import BuildDocDebugMessage, BuildDocError, BuildDocTracedError, BuildDocTracedWarning


class Parser:
    """ Parses the tokens from the lexer. """

    def __init__(self, flags: Flags) -> None:
        self.status_code, self.verbose = 1 if not flags.always_zero else 0, flags.verbose

    def raise_unexpected_token(self, token: Token | LetterToken | NumberToken | UnknownToken | StringToken | Variable | EnvVariable | Macro, line: int, char: int):
        value = "whitespace" if token.value == ' ' else "newline" if token.value == '\n' else "tab" if token.value == '\t' else "'%s'" %token.value
        raise BuildDocTracedError("unexpected %s" %value, self.status_code, line, char)

    @staticmethod
    def parse_string(string:str, line: int, vars_map: dict[str, tuple[str, bool]], flags: Flags) -> str:
        parsed_string = string

        potentially_reading_shell_var = False
        reading_var, reading_env_var, reading_shell_var = False, False, False
        var, env_var, shell_var = '', '', ''
        vars_in_str: list[Variable | EnvVariable | ShellVariable] = []

        for c in range(len(string)):
            char = string[c]

            if reading_var:
                if char.lower() in Token.LETTER.value or char == Token.UNDERSCORE.value: var += char
                else:
                    vars_in_str.append(Variable(var, line, c, 0 if flags.always_zero else 1))
                    var, reading_var = '', False

            elif reading_env_var:
                if char.lower() in Token.LETTER.value or char in Token.NUMBER.value or char == Token.UNDERSCORE.value: env_var += char
                else:
                    vars_in_str.append(EnvVariable(env_var, line, c, 0 if flags.always_zero else 1))
                    env_var, reading_env_var = '', False

            elif potentially_reading_shell_var and not reading_shell_var:
                if char == Token.L_BRACE.value: reading_shell_var = True
                else: potentially_reading_shell_var = False

            elif reading_shell_var:
                if not char == Token.R_BRACE.value: shell_var += char
                else:
                    vars_in_str.append(ShellVariable(shell_var, line, c, 0 if flags.always_zero else 1))
                    shell_var, reading_shell_var, potentially_reading_shell_var = '', False, False

            match char:
                case Token.DOLLAR.value: reading_var = True
                case Token.AT.value: reading_env_var = True
                case Token.QUESTION.value: potentially_reading_shell_var = True

            if c == len(string)-1:
                if len(var) > 0: vars_in_str.append(Variable(var, line, c, 0 if flags.always_zero else 1))
                if len(shell_var) > 0: vars_in_str.append(ShellVariable(shell_var, line, c, 0 if flags.always_zero else 1))

        for v in range(len(vars_in_str)):
            varobj = vars_in_str[v]

            if type(varobj) is Variable:
                if len(varobj.var_name) > 0:
                    value, constant = varobj.value(vars_map)
                    val = Parser.parse_string(value, line, vars_map, flags)  # 🔄!
                    parsed_string = parsed_string.replace("$%s" %varobj.var_name, val)

            elif type(varobj) is EnvVariable: parsed_string = parsed_string.replace("@%s" %varobj.var_name, varobj.value())
            elif type(varobj) is ShellVariable: parsed_string = parsed_string.replace("?{%s}" %varobj.cmd, varobj.value()).replace('\n', '', 1)

        if len(var) > 0 or len(env_var) > 0:
            if reading_var:
                try:
                    value, constant = vars_map[var]
                    val = Parser.parse_string(value, line, vars_map, flags)  # 🔄!
                    parsed_string = parsed_string.replace("$%s" %var, val)
                except: raise BuildDocTracedError("'%s' is undefined" %var, 0 if flags.always_zero else 1, line+1, len(var))

            elif reading_env_var:
                value = environ[env_var] if env_var in environ else ''
                parsed_string = parsed_string.replace("@%s" %env_var, value)

        return parsed_string

    @staticmethod
    def validate_conditional_syntax(statement: str, always_zero: bool) -> str | None:
        """ Ensures the syntax for an `if` or `elif` statement is valid, returning the condition if it is. """

        condition, operator = '', ''
        paren_open = False
        code = 0 if always_zero else 1

        for _c in range(len(statement)):
            c = statement[_c]

            if _c < 1 and c == Token.AMPERSAND.value: return None

            if paren_open:
                if c == Token.R_PAREN.value: paren_open = False
                elif c == Token.L_PAREN.value: raise BuildDocError("unexpected '('.", code)
                else: condition += c

            else:
                if not c == Token.WHITESPACE.value: operator += c
                if c == Token.L_PAREN.value: paren_open = True
                if c == Token.R_PAREN.value: raise BuildDocError("unexpected ')'.", code)

        if paren_open: raise BuildDocError("unclosed '('.", code)
        if len(condition) < 1: raise BuildDocError("Empty condition.", 1)

        return condition

    @staticmethod
    def evaluate_condition(condition: str, status: int, verbose: bool) -> bool:
        """ Evaluates the condition in the `if` or `elif` statement to true or false. """

        l_operand, logic_word, r_operand = '', '', ''
        bracket_open = False
        spaces = 0


        for _c in range(len(condition)):
            c = condition[_c]

            match c:
                case Token.WHITESPACE.value:
                    if len(l_operand) < 1: raise BuildDocError("unexpected whitespace.", status)
                    else:
                        if not bracket_open: spaces += 1

                # case Token.L_PAREN.value, Token.L_BRACK.value, Token.L_BRACE.value:
                #     if bracket_open: raise BuildDocError(f"unexpected '{c}'", status)
                #     else: bracket_open = True

                # case Token.R_PAREN.value, Token.R_BRACK.value, Token.R_BRACE.value:
                #     if not bracket_open: raise BuildDocError(f"unexpected '{c}'", status)
                #     else: bracket_open = False

                case c:
                    if spaces < 1: l_operand += c
                    elif spaces > 0 and spaces < 2: logic_word += c
                    else: r_operand += c

        if verbose: BuildDocDebugMessage(f"l_operand = {l_operand} | logic_word = {logic_word} | r_operand = {r_operand}")

        match logic_word:
            case "is": return l_operand == r_operand
            case "isnt": return not l_operand == r_operand
            case "greater": return l_operand > r_operand
            case "less":  return l_operand < r_operand
            case c: raise BuildDocError("'%s' is not a valid logic word." %logic_word, status)

    def map(self, tokens: list[Token | LetterToken | NumberToken | UnknownToken | StringToken | Variable | EnvVariable | Macro]):
        """ Maps variables with their values, and tasks with their commands. """

        if self.verbose: BuildDocDebugMessage("TOKENS: %s" %([t.name for t in tokens]))

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
        task_map: dict[str, tuple[list[tuple[str | Macro, int]], bool]] = {}

        # Ensuring line 1 doesn't start with a whitespace or tab.
        if tokens[0] is Token.WHITESPACE or tokens[0] is Token.TAB: self.raise_unexpected_token(tokens[0], 1, 1)

        # Iterate over every token.
        for t in range(len(tokens)):
            char += 1
            token = tokens[t]
            astr_open = dstr_open or sstr_open

            if token is Token.NEWLINE:
                if self.verbose: BuildDocDebugMessage(f"Line {line} -> {line+1}")
                line += 1
                char = 0

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

                            if current_section in task_map: raise BuildDocError("duplicate task: '%s'." %current_section, self.status_code)

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
                                if self.verbose: BuildDocDebugMessage("COMMAND = %s" %cmd)
                                if cmd == "macro": ...
                                else: task_map[current_section][0].append((cmd, line+3))
                                command = ''

                            var_name, var_value = '', ''
                            reading_var_value = False

                        case Token.BROKEN_STR: raise BuildDocTracedError("unclosed string", self.status_code, line, char)

                        case Token.SOF as tok: ...

                        case Token.EOF as tok:
                            if bracket_open: raise BuildDocTracedError("unclosed '['", self.status_code, line, char)
                            if astr_open: raise BuildDocTracedError("unclosed string", self.status_code, line, char)

                        # OTHER #
                        case tok if type(tok) is Variable:
                            value, constant = tok.value(vars_map)

                            if self.verbose: BuildDocDebugMessage("value: %s" %value)
                            if self.verbose: BuildDocDebugMessage("constant: %s" %("yes" if constant else "no"))

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

                        case t if type(t) is Macro: task_map[current_section][0].append((t, line))

                        case _: ...

        if self.verbose: BuildDocDebugMessage("VARS MAP: %s" %vars_map)
        if self.verbose: BuildDocDebugMessage("TASK MAP: %s" %task_map)
        return (vars_map, task_map)
