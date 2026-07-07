# src/twip/behavior/eatable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Eatable(MessageAction):
    kind: ClassVar[str] = "eatable"
    verb: ClassVar[str] = "eat"