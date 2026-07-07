# src/twip/extension/tasteable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Tasteable(MessageAction):
    kind: ClassVar[str] = "tasteable"
    verb: ClassVar[str] = "taste"