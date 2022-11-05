from interpreter.tokens import *


class Lexer:
    """ Tokenizes the code. """

    @staticmethod
    def tokenize(code: list[str]) -> list[Token | LetterToken | NumberToken | UnknownToken | StringToken]:
        tokens: list[Token | LetterToken | NumberToken | UnknownToken | StringToken] = []
        string, sstr_open, dstr_open = '', False, False

        tokens.append(Token.SOF)

        # Iterate over each line.
        for line in range(len(code)):
            # tokens.append(Token.NEWLINE)

            # Iterate over each character in the current line.
            for c in range(len(code[line])):
                cc = code[line][c]  # Current character.

                # Reading strings here to make it easier for the parser.
                if cc == Token.S_QUOTE.value and not dstr_open:  # Single quote strings.
                    sstr_open = not sstr_open
                    if not sstr_open: tokens.append(StringToken(string)); string = ''

                elif cc == Token.D_QUOTE.value and not sstr_open:  # Double quote strings.
                    dstr_open = not dstr_open
                    if not dstr_open: tokens.append(StringToken(string)); string = ''

                elif sstr_open or dstr_open: string += cc

                # `Token.LETTER` & `Token.NUMBER` are both of type `list[str]`, so they can't be used as cases.
                elif cc in Token.LETTER.value: tokens.append(LetterToken(cc))
                elif cc in Token.NUMBER.value: tokens.append(NumberToken(cc))
                else:
                    try: tokens.append(Token(cc))  # `Token(cc)` will find whatever Token has the value matching `cc`.
                    except ValueError: tokens.append(UnknownToken(cc))  # Tells the parser to ignore this token in certain circumstances.

        if len(string) > 0: tokens.append(StringToken(string))
        tokens.append(Token.EOF)

        print([t.name for t in tokens])
        return tokens
