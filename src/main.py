from flags import Flags
from out import BuildDocError
from pathlib import Path


if __name__ == "__main__":
  Flags().init()  # Initialize Flags.

  # Check if there is a BuildDoc in cwd.
  if not ((cwd:=Path().cwd())/"BuildDoc").exists(): raise BuildDocError("No BuildDoc in `%s`." %cwd, 1)
  # if Flags.givens["verbose"]: ...

  # Invoke the lexer and get the ball rolling!
  ...
