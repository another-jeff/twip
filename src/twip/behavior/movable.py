# src/twip/behavior/movable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Movable(VerbMessageBehavior):
    kind: ClassVar[str] = "movable"
    verb: ClassVar[str] = "move"