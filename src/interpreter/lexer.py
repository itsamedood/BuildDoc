from interpreter.flags import Flags
from interpreter.tokens import Token
from out import BuildDocDebugMessage


class Lexer:
    def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

    def tokenize(self, _code: str) -> list[tuple[Token, str | int | None]]:
        tokens: list[tuple[Token, str | int | None]] = []

        for cc in _code:
            try: tokens.append((Token(cc), cc))
            except ValueError:
                if cc.isalpha(): tokens.append((Token.LETTER, cc))
                elif cc.isalnum(): tokens.append((Token.NUMBER, cc))
                else: tokens.append((Token.UNKNOWN, cc))
        tokens.append((Token.EOF, None))

        if self.FLAGS.verbose: BuildDocDebugMessage("Tokens: %s" %tokens)
        return tokens
