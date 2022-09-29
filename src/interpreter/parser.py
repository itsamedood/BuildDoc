from interpreter.tokens import LetterToken, NumberToken, Token
from out import BuildDocTracedError


class Parser:
    """
    Parses the tokens from the lexer.
    """

    @staticmethod
    def map(tokens: list[Token | LetterToken | NumberToken]):
        line, char = 1, 0
        var_name, var_value = "", ""
        section, current_section = "", ""
        parenth_open, bracket_open, brace_open = False, False, False

        vars_map: dict[str, str] = {}
        task_map: dict[str, list[str]] = {}

        for t in range(len(tokens)):
            char += 1
            token = tokens[t]

            match token:
                case Token.NEWLINE:
                    line += 1
                    char = 0

                case Token.HASH:
                    pass

                case Token.L_BRACK:  # Opening for section.
                    bracket_open = True

                case Token.R_BRACK:  # Closing for section.
                    if not bracket_open:
                        raise BuildDocTracedError("unopened bracket", 1, line, char)
                    if len(section) < 1:
                        raise BuildDocTracedError("no section name given", 1, line, char)

                    current_section, section = section, ""
                    print(f"In: {current_section}")  # For testing, will be removed.
                    bracket_open = False

                case _ if type(token) is LetterToken:
                    if bracket_open:
                        section += token.value

        return (vars_map, task_map)
