from enum import Enum
from typing import Any


class Token(Enum):
  """
  All valid tokens/characters in BuildDoc.

  Comments bypass this entirely, meaning you can use emojis or other languages.
  """

  ANY         = Any
  LETTER      = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
  NUMBER      = b'0123456789'
  EXCLAMATION = b'!'
  AT          = b'@'
  POUND       = b'#'
  DOLLAR      = b'$'
  PERCENT     = b'%'
  CARET       = b'^'
  AMPERSAND   = b'&'
  UNDERSCORE  = b'_'
  PLUS        = b'+'
  HYPHEN      = b'-'
  ASTERISK    = b'*'
  SLASH       = b'/'
  EQUAL       = b'='
  L_PARENTH   = b'('
  R_PARENTH   = b')'
  L_BRACE     = b'{'
  R_BRACE     = b'}'
  L_BRACKET   = b'['
  R_BRACKET   = b']'
  L_ANGLE     = b'<'
  R_ANGLE     = b'>'
  COMMA       = b','
  PERIOD      = b'.'
  COLON       = b':'
  SEMICOLON   = b';'
  QUESTION    = b'?'
  PIPELINE    = b'|'
  BACKSLASH   = b'\\'
  TILDE       = b'~'
  BACKTICK    = b'`'
  D_QUOTE     = b'"'
  S_QUOTE     = b"'"
