# src/twip/behavior/tasteable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Tasteable(MessageAction):
    kind: ClassVar[str] = "tasteable"
    verb: ClassVar[str] = "taste"