# src/twip/behavior/listenable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Listenable(VerbMessageBehavior):
    kind: ClassVar[str] = "listenable"
    verb: ClassVar[str] = "listen"