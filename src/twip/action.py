# src/twip/action.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    verb: str = ""
    target: str = ""
    text: str = ""
    preposition: str = ""
    target_indirect: str = ""