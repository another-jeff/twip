# src/twip/behavior/pushable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Pushable(VerbMessageBehavior):
    kind: ClassVar[str] = "pushable"
    verb: ClassVar[str] = "push"