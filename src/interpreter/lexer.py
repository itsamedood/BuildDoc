from interpreter.tokens import *
from interpreter.flags import Flags
from interpreter.variable import Variable
from out import BuildDocNote


class Lexer:
    """ Tokenizes the code. """

    @staticmethod
    def tokenize(code: list[str], flags: Flags):
        tokens: list[Token | LetterToken | NumberToken | UnknownToken | StringToken | Variable] = []
        string, var_name = '', ''
        sstr_open, dstr_open, reading_var, comment = False, False, False, False

        # verbose: bool, status_code: int
        verbose, status_code = flags.verbose, 0 if flags.always_zero else 1

        tokens.append(Token.SOF)

        if verbose: BuildDocNote("iterating over each line")

        # Iterate over each line.
        for line in range(len(code)):
            if verbose: BuildDocNote("iterating through each char on line %s." %(line+1))

            # Iterate over each character in the current line.
            for c in range(len(code[line])):
                cc = code[line][c]  # Current character.

                if comment:
                    if cc == Token.NEWLINE.value: comment = False
                    else: continue

                elif cc == Token.HASH.value: comment = True

                # Reading strings here to make it easier for the parser.
                if cc == Token.S_QUOTE.value and not dstr_open:  # Single quote strings.
                    sstr_open = not sstr_open
                    if not sstr_open: tokens.append(StringToken(string)); string = ''

                elif cc == Token.D_QUOTE.value and not sstr_open:  # Double quote strings.
                    dstr_open = not dstr_open
                    if not dstr_open: tokens.append(StringToken(string)); string = ''

                elif sstr_open or dstr_open: string += cc

                elif reading_var:
                    if cc.lower() in Token.LETTER.value: var_name += cc
                    else:
                        tokens.append(Variable(var_name, line, c, status_code))
                        reading_var = False
                        var_name = ''

                elif cc == Token.DOLLAR.value:
                    reading_var = True

                # `Token.LETTER` & `Token.NUMBER` are both of type `list[str]`, so they can't be used as cases.
                elif cc.lower() in Token.LETTER.value: tokens.append(LetterToken(cc))
                elif cc in Token.NUMBER.value: tokens.append(NumberToken(cc))
                else:
                    try: tokens.append(Token(cc))  # `Token(cc)` will find whatever Token has the value matching `cc`.
                    except ValueError: tokens.append(UnknownToken(cc))  # Tells the parser to ignore this token in certain circumstances.

                if verbose: BuildDocNote("Appended token: %s" %tokens[-1].name)

        if len(string) > 0: tokens.append(Token.BROKEN_STR)
        tokens.append(Token.EOF)

        if verbose: BuildDocNote("FINAL TOKENS:\n%s" %[t.name for t in tokens])
        return tokens
