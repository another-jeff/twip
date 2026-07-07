# src/twip/behavior/turnable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Turnable(VerbMessageBehavior):
    kind: ClassVar[str] = "turnable"
    verb: ClassVar[str] = "turn"