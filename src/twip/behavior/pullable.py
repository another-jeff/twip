# src/twip/behavior/pullable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Pullable(VerbMessageBehavior):
    kind: ClassVar[str] = "pullable"
    verb: ClassVar[str] = "pull"