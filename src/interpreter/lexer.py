from interpreter.tokens import Token


class Lexer:
    def __init__(self) -> None: ...

    def tokenize(self) -> list[tuple[Token, str | int | None]]:
        tokens: list[tuple[Token, str | int | None]] = []

        ...

        return tokens
