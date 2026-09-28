from interpreter.token import Token
from out import BuildDocDebugMessage, BuildDocError


class Lexer:
  """
  Tokenizes the script into tokens for the parser. Ignores comments.
  """

  tokens: list[list[tuple[Token, str]]] = []
  comment = False

  def __init__(self) -> None: ...

  def tokenize(self, code: list[str]) -> list[list[tuple[Token, str]]]:
    """
    Tokenizes code into tokens (duh) for the parser. Returns `self.tokens`.

    Ignores comments entirely.
    """

    # final_tokens: list[list[tuple[Token, str]]] = []
    tokline: list[tuple[Token, str]] = []

    for linenum, line in enumerate(code):
      # BuildDocDebugMessage(line)
      for char in line:
        try:
          if char == Token.POUND.value: break  # Skip the entire rest of the line or the entire line at that.

          tokline.append(
            (Token.LETTER, char) if char in Token.LETTER.value else
            (Token.NUMBER, char) if char in Token.NUMBER.value else
            (Token(char), char)
          )

        except ValueError:
          tokline.append((Token.ANY, char))  # Handle later in the parser.

      # BuildDocDebugMessage(tokline)

      self.tokens.append(tokline)
      # tokline.clear()

    [[BuildDocDebugMessage(t.name, v) for t,v in l] for l in [_ for _ in self.tokens]]
    # BuildDocDebugMessage([[(t.name, v) for t,v in l] for l in [_ for _ in self.tokens]])
    return self.tokens

    # for char in code:
    #   try:
    #     # Probably gonna be more important later on.
    #     if char == Token.NEWLINE.value:
    #       self.comment = False
    #       # Maybe not 2 steps ahead after all.

    #     if char == Token.POUND.value:
    #       self.comment = True
    #       continue

    #     if self.comment: continue

    #     self.tokens.append(
    #       (Token.LETTER, char) if char in Token.LETTER.value else
    #       (Token.NUMBER, char) if char in Token.NUMBER.value else
    #       (Token(char), char)
    #     )
    #   except ValueError:
    #     self.tokens.append((Token.ANY, char))  # Handle later since `echo 👌` should work.
        # raise BuildDocError("Unknown character: '%s'." %char, 1)

    # return self.tokens
