from collections.abc import Callable, Iterable


def ask(prompts: Iterable[str], read: Callable[[str], str] = input) -> list[str]:
    return [read(f"{p}: ") for p in prompts]
