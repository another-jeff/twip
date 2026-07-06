# src/twip/action.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    verb: str
    target: str = ""
    text: str = ""
    preposition: str = ""
    indirect_target: str = ""