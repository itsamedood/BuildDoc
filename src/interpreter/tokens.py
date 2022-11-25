from enum import Enum


class LetterToken:
    def __init__(self, letter: str) -> None: self.value, self.name = letter, "LETTER"


class NumberToken:
    def __init__(self, number: str) -> None: self.value, self.name = number, "NUMBER"


class UnknownToken:
    def __init__(self, token: str) -> None: self.value, self.name = token, "UNKNOWN"


class StringToken:
    def __init__(self, string: str) -> None: self.value, self.name = string, "STRING"


class Token(Enum):
    # LISTS #
    LETTER      = [c for c in "abcdefghijklmnopqrstuvwxyz"]
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
    BROKEN_STR  = ''
    SOF         = ...
    EOF         = None
