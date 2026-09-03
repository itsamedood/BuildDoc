from interpreter.token import Token
from out import BuildDocError


class Lexer:
  """
  Tokenizes the script into tokens for the parser. Ignores comments.
  """

  tokens: list[tuple[Token, str]]
  comment = False

  def __init__(self) -> None: ...

  def tokenize(self, code: str) -> None: # Iterator[Token]:
    """
    Tokenizes code into tokens (duh) for the parser.

    Ignores comments entirely.
    """

    for char in code:
      try:
        # Probably gonna be more important later on.
        if char == Token.NEWLINE.value:
          self.comment = False
          ...  # 2 steps ahead?

        if char == Token.POUND.value:
          self.comment = True
          continue

        if self.comment: continue

        self.tokens.append(
          (Token.LETTER, char) if char in Token.LETTER.value else
          (Token.NUMBER, char) if char in Token.NUMBER.value else
          (Token(char), char)
        )
      except ValueError:
        raise BuildDocError("Unknown character: '%s'." %char, 1)
        # self.tokens.append((Token.ANY, char))
