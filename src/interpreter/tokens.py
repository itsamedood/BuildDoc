from enum import Enum


class Token(Enum):
    LETTER = 'a'
    NUMBER = 'n'

    # Brackets #
    L_PAREN         = '('
    R_PAREN         = ')'
    L_BRACE         = '{'
    R_BRACE         = '}'
    L_BRACKET       = '['
    R_BRACKET       = ']'
    L_ANGLE_BRACKET = '<'
    R_ANGLE_BRACKET = '>'

    # Operators #
    DOLLAR          = '$' # Variables.
    AT              = '@' # Environmental variables.
    QUESTION_MARK   = '?' # Shell commands.
    AMPERSAND       = '&' # Silences a command.
    PERCENT         = '%' # Macros.
    EQUAL           = '=' # Variable assignment.

    # Symbols #
    HASH            = '#' # Comment.
    D_QUOTE         = '"'
    S_QUOTE         = '\"'
    BACKTICK        = '`'
    PERIOD          = '.'
    COMMA           = ','
    HYPHEN          = '-'
    UNDERSCORE      = '_'
    PIPELINE        = '|'
    EXCLAMATION     = '!'
    COLON           = ':'
    SEMICOLON       = ';'
    CAROT           = '^'
    ASTERISK        = '*'
    TILDE           = '~'
    FORWARD_SLASH   = '/'
    BACKWARD_SLASH  = '\\'

    # Other #
    WHITESPACE      = ' '
    TAB             = '\t'
    NEWLINE         = '\n'
    BROKEN_STR      = ''
    UNKNOWN         = None
    EOF             = None
