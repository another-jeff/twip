# src/twip/behavior/readable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Readable(VerbMessageBehavior):
    kind: ClassVar[str] = "readable"
    verb: ClassVar[str] = "read"