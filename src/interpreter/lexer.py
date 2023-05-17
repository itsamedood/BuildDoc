from interpreter.tokens import *
from interpreter.variable import *
from interpreter.flags import Flags
from interpreter.macro import Macro
from out import BuildDocDebugMessage, BuildDocTracedError


class Lexer:
    """ Tokenizes the code. """

    @staticmethod
    def tokenize(code: list[str], flags: Flags):
        tokens: list[Token | LetterToken | NumberToken | UnknownToken | StringToken | Variable | EnvVariable | Macro] = []
        macro_args: list[str] = []
        string, var_name, env_var_name, macro_name, macro_arg = '', '', '', '', ''
        sstr_open, dstr_open, paren_open = False, False, False
        comment = False
        reading_var, reading_env_var, reading_macro = False, False, False

        verbose, status_code = flags.verbose, 0 if flags.always_zero else 1

        tokens.append(Token.SOF)
        if verbose: BuildDocDebugMessage("iterating over each line...")

        # Iterate over each line.
        for line in range(len(code)):
            if verbose: BuildDocDebugMessage("iterating through each char on line %s." %(line+1))

            # Iterate over each character in the current line.
            for c in range(len(code[line])):
                cc = code[line][c]  # Current character.

                if comment:
                    if cc == Token.NEWLINE.value: comment = False
                    else: continue

                elif reading_var:
                    if cc.lower() in Token.LETTER.value or cc == Token.UNDERSCORE.value: var_name += cc
                    else:
                        tokens.append(Variable(var_name, line, c, status_code))
                        reading_var = False
                        var_name = ''

                        # Ensures that whatever character ended reading the variable name is added to the list.
                        if cc.lower() in Token.LETTER.value: tokens.append(LetterToken(cc))
                        elif cc in Token.NUMBER.value: tokens.append(NumberToken(cc))
                        else:
                            try: tokens.append(Token(cc))
                            except ValueError: tokens.append(UnknownToken(cc))

                    if not cc == Token.NEWLINE.value: continue

                elif reading_env_var:
                    if cc.lower() in Token.LETTER.value or cc in Token.NUMBER.value or cc == Token.UNDERSCORE.value: env_var_name += cc
                    else:
                        tokens.append(EnvVariable(env_var_name, line, c, status_code))

                elif reading_macro:
                    if flags.verbose: BuildDocDebugMessage("Macro name: %s" %macro_name)
                    if flags.verbose: BuildDocDebugMessage("Macro args: %s" %macro_args)

                    if not paren_open:
                        if cc in Token.LETTER.value: macro_name += cc
                        elif cc == Token.L_PAREN.value: paren_open = True
                        else: raise BuildDocTracedError("unexpected '%s'", 0 if flags.always_zero else 1, line, c+1)
                    else:
                        if cc == Token.R_PAREN.value:
                            if len(macro_arg) > 0: macro_args.append(macro_arg)
                            tokens.append(Macro(macro_name, macro_args, line, flags, None, None))

                            reading_macro, paren_open, macro_name, macro_arg, macro_args, = False, False, '', '', []

                        elif not cc == Token.COMMA.value: macro_arg += cc
                        else:
                            macro_args.append(macro_arg)
                            macro_arg = ''

                elif cc == Token.HASH.value: comment = True
                else:
                    # Reading strings here to make it easier for the parser.
                    if cc == Token.S_QUOTE.value and not dstr_open:  # Single quote strings.
                        sstr_open = not sstr_open
                        if not sstr_open: tokens.append(StringToken(string)); string = ''

                    elif cc == Token.D_QUOTE.value and not sstr_open:  # Double quote strings.
                        dstr_open = not dstr_open
                        if not dstr_open: tokens.append(StringToken(string)); string = ''

                    elif sstr_open or dstr_open: string += cc
                    elif cc == Token.DOLLAR.value: reading_var = True
                    elif cc == Token.AT.value: reading_env_var = True
                    elif cc == Token.PERCENT.value: reading_macro = True

                    # `Token.LETTER` & `Token.NUMBER` are both of type `list[str]`, so they can't be used as cases.
                    elif cc.lower() in Token.LETTER.value: tokens.append(LetterToken(cc))
                    elif cc in Token.NUMBER.value: tokens.append(NumberToken(cc))
                    else:
                        try: tokens.append(Token(cc))  # `Token(cc)` will find whatever Token has the value matching `cc`.
                        except ValueError: tokens.append(UnknownToken(cc))  # Tells the parser to ignore this token in certain circumstances.

                    if verbose: BuildDocDebugMessage("Appended token: %s" %tokens[-1].name)

        if len(string) > 0: tokens.append(Token.BROKEN_STR)
        tokens.append(Token.EOF)

        return tokens
