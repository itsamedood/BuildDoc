from interpreter.flags import Flags
from out import BuildDocDebugMessage


class Evaluator:
  """ Evaluates conditional logic because `eval()` can easily lead to ACE. """

  def __init__(self, _flags: Flags) -> None:
    self.FLAGS = _flags

  def evaluate(self, _cond: str) -> bool:
    """ Evaluates if `_cond` (stripped) is `True` or `False`. """

    BuildDocDebugMessage("READING IF STATEMENT", _verbose=self.FLAGS.verbose)

    operations = []
    l_parens, r_parens, s_quotes, d_quotes = 0, 0, 0, 0
    result = False

    # I'm gonna be here for a while...
    for i, c in enumerate(_cond):
      ...

    return result
