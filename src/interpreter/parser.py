from interpreter.flags import Flags
from interpreter.tokens import Token


class Parser:
    def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

    def parse_tokens(self, _tokens: list[tuple[Token, str | int | None]]):
        for t in range(len(_tokens)):
            token, value = _tokens[t]
