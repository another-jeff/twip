# src/twip/behavior/movable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Movable(MessageAction):
    kind: ClassVar[str] = "movable"
    verb: ClassVar[str] = "move"