# src/twip/behavior/tasteable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Tasteable(VerbMessageBehavior):
    kind: ClassVar[str] = "tasteable"
    verb: ClassVar[str] = "taste"