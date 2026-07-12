# src/twip/play.py

from __future__ import annotations

from collections.abc import Callable

from twip.world import World


def play(
    world: World,
    *,
    read: Callable[[str], str] = input,
    write: Callable[[str], None] = print,
) -> None:
    while True:
        try:
            text = read("> ")
        except (EOFError, KeyboardInterrupt):
            write("")
            return

        text = text.strip()

        if not text:
            continue

        if text.casefold() in {"quit", "exit"}:
            return

        result = world.handle(text)
        write(result.message)