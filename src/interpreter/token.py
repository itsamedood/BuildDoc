from enum import Enum
from typing import Any


class Token(Enum):
  """
  All valid tokens/characters in BuildDoc.

  Comments bypass this entirely, meaning you can use emojis or other languages.
  """

  ANY         = Any
  LETTER      = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  NUMBER      = '0123456789'
  EXCLAMATION = '!'
  AT          = '@'
  POUND       = '#'
  DOLLAR      = '$'
  PERCENT     = '%'
  CARET       = '^'
  AMPERSAND   = '&'
  UNDERSCORE  = '_'
  PLUS        = '+'
  HYPHEN      = '-'
  ASTERISK    = '*'
  SLASH       = '/'
  EQUAL       = '='
  L_PARENTH   = '('
  R_PARENTH   = ')'
  L_BRACE     = '{'
  R_BRACE     = '}'
  L_BRACKET   = '['
  R_BRACKET   = ']'
  L_ANGLE     = '<'
  R_ANGLE     = '>'
  COMMA       = ','
  PERIOD      = '.'
  COLON       = ':'
  SEMICOLON   = ';'
  QUESTION    = '?'
  PIPELINE    = '|'
  BACKSLASH   = '\\'
  TILDE       = '~'
  BACKTICK    = '`'
  D_QUOTE     = '"'
  S_QUOTE     = "'"
  SPACE       = ' '
  TAB         = '\t'
  NEWLINE     = '\n'
  CARRIAGE    = '\r'
