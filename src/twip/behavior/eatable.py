# src/twip/behavior/eatable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Eatable(VerbMessageBehavior):
    kind: ClassVar[str] = "eatable"
    verb: ClassVar[str] = "eat"