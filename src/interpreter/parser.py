from interpreter.ast import AST
from interpreter.flags import Flags
from interpreter.tokens import Token


class Parser:
    def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

    def parse_tokens(self, _tokens: list[tuple[Token, str | int | None]]) -> AST:
        TREE = AST()

        for i, t in enumerate(_tokens):
            token, value = t

        return TREE
