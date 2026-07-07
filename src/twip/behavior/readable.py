# src/twip/behavior/readable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Readable(MessageAction):
    kind: ClassVar[str] = "readable"
    verb: ClassVar[str] = "read"