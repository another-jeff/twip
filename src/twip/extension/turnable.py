# src/twip/extension/turnable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Turnable(MessageAction):
    kind: ClassVar[str] = "turnable"
    verb: ClassVar[str] = "turn"