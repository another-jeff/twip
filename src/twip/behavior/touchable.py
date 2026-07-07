# src/twip/behavior/touchable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Touchable(MessageAction):
    kind: ClassVar[str] = "touchable"
    verb: ClassVar[str] = "touch"