from enum import Enum
from typing import Any


class Token(Enum):
  LETTER      = Any
  NUMBER      = Any
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
