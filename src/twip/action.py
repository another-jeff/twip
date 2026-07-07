# src/twip/action.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    verb: str
    text: str
    target: str | None = None
    preposition: str | None = None
    target_indirect: str | None = None