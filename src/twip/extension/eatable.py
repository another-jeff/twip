# src/twip/extension/eatable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Eatable(MessageAction):
    kind: ClassVar[str] = "eatable"
    verb: ClassVar[str] = "eat"