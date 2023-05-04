from out import BuildDocError


class Flags:
    """ Represents flags passed in through the command line. """
    def __init__(self, flags: list[str] | None) -> None:
        self.allow_recursion = False
        self.always_zero = False
        self.no_echo = False
        self.verbose = False
        self.display_help = False
        self.init = False

        for flag in flags if flags is not None else []:
            match flag[2:]:
                case "allow-recursion": self.allow_recursion = True
                case "always-zero": self.always_zero = True
                case "no-echo": self.no_echo = True
                case "verbose": self.verbose = True
                case "help" if flags is not None and len(flags) < 2: self.display_help = True,
                case "init" if flags is not None and len(flags) < 2: self.init = True
                case flag: raise BuildDocError("unknown flag: '%s'" %flag, self.always_zero)
