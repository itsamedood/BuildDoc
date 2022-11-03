from enum import Enum


class LetterToken:
    """ Used with `Token.LETTER`. """

    value = ''

    def __init__(self, letter: str) -> None: self.value = letter

class NumberToken:
    """ Used with `Token.NUMBER`. """

    value = ''

    def __init__(self, number: str) -> None: self.value = number


class UnknownToken:
    """ Represents an unknown token, such as a unicode character, or unused symbol like caret (^). """

    value = ''

    def __init__(self, token: str) -> None: self.value = token

class Token(Enum):
    """ Represents a token from the Lexer. """

    # LISTS #
    LETTER      = [c for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    NUMBER      = [n for n in "0123456789"]

    # PAIRS #
    L_PAREN     = '('
    R_PAREN     = ')'
    L_BRACE     = '{'
    R_BRACE     = '}'
    L_BRACK     = '['
    R_BRACK     = ']'
    L_ANG_BRACK = '<'
    R_ANG_BRACK = '>'

    # OPERATORS #
    DOLLAR      = '$'  # Variables.
    AT          = '@'  # Environmental variables.
    QUESTION    = '?'  # Shell commands.
    AMPERSAND   = '&'  # & = Silence. && = Logical AND.
    PERCENT     = '%'  # Macros.
    EQUAL       = '='  # Assignment.

    # SYMBOLS #
    HASH        = '#'  # Comment.
    D_QUOTE     = '"'
    S_QUOTE     = '\''
    BACKTICK    = '`'
    PERIOD      = '.'
    COMMA       = ','
    DASH        = '-'
    UNDERSCORE  = '_'
    PIPELINE    = '|'  # | = Passing the result of a command to another. || = Logical OR.

    # SPECIAL #
    WHITESPACE  = ' '
    BACKSLASH   = '\\'
    TAB         = '\t'
    NEWLINE     = '\n'
    EOF         = None
