from interpreter.tokens import *


class Lexer:
    """ Tokenizes the code. """

    @staticmethod
    def tokenize(code: list[str]) -> list[Token | LetterToken | NumberToken | UnknownToken]:
        tokens: list[Token | LetterToken | NumberToken | UnknownToken] = []

        # Iterate over each line.
        for line in range(len(code)):
            tokens.append(Token.NEWLINE)

            # Iterate over each character in the current line.
            for c in range(len(code[line])):
                cc = code[line][c]  # Current character.

                # `Token.LETTER` & `Token.NUMBER` are both of type `list[str]`, so they can't be used as cases.
                if cc in Token.LETTER.value: tokens.append(LetterToken(cc))
                elif cc in Token.NUMBER.value: tokens.append(NumberToken(cc))
                else:
                    try: tokens.append(Token(cc))  # `Token(cc)` will find whatever Token has the value matching `cc`.
                    except ValueError: tokens.append(UnknownToken(cc))  # Tells the parser to ignore this token in certain circumstances.
        return tokens
