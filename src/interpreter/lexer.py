from interpreter.flags import Flags
from interpreter.tokens import Token
from out import BuildDocDebugMessage


class Lexer:
    def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

    def tokenize(self, _code: str) -> list[tuple[Token, str | int | None]]:
        tokens: list[tuple[Token, str | int | None]] = []

        for c in range(len(_code)):
            cc = _code[c]

            try: tokens.append((Token(cc), cc))
            except ValueError: tokens.append((Token.UNKNOWN, cc))

        if self.FLAGS.verbose: BuildDocDebugMessage("Tokens: %s" %tokens)
        return tokens
