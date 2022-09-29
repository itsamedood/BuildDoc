class Runner:
    """
    Responsible for running tasks and handling errors.
    """

    @staticmethod
    def run_task(task: str | None, dicts: tuple[dict[str, str], dict[str, list[str]]]) -> None:
        # 👇 The parser isn't done, so the dicts are always empty. For testing purposes, this issue is ignored like so.
        try:
            vars_map = dicts[0]
            cmds_map = dicts[1][task] if task is not None else dicts[1][[t for t in dicts[1]][0]]
        except IndexError:
            pass
