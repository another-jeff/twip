# src/twip/behavior/touchable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Touchable(VerbMessageBehavior):
    kind: ClassVar[str] = "touchable"
    verb: ClassVar[str] = "touch"