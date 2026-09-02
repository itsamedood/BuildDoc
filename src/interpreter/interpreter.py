from pathlib import Path


class Interpreter:
  def __init__(self, path: Path) -> None:
    with open(path, "rb") as script:
      self.raw = script.read()

    ...
