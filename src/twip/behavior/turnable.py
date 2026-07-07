# src/twip/behavior/turnable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Turnable(MessageAction):
    kind: ClassVar[str] = "turnable"
    verb: ClassVar[str] = "turn"