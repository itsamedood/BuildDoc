from interpreter.flags import Flags
from interpreter.tokens import Token
from out import BuildDocDebugMessage


class Lexer:
  """ Tokenizes the code for the parser. """

  def __init__(self, _flags: Flags) -> None: self.FLAGS = _flags

  def tokenize(self, _code: str) -> list[tuple[Token, str | int | None]]:
    tokens: list[tuple[Token, str | int | None]] = []

    for cc in _code:
      # Attempt to find a token in the enum, falling to logic on exception.
      try: tokens.append((Token(cc), cc))
      except ValueError:
        # Determine if the token is a letter, number, or unknown.
        if cc.isalpha(): tokens.append((Token.LETTER, cc))
        elif cc.isalnum(): tokens.append((Token.NUMBER, cc))
        else: tokens.append((Token.UNKNOWN, cc))
    tokens.append((Token.EOF, None))

    if self.FLAGS.verbose: BuildDocDebugMessage("TOKENS: %s" %tokens, _verbose=self.FLAGS.verbose)
    return tokens
