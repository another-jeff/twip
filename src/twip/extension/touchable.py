# src/twip/extension/touchable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Touchable(MessageAction):
    kind: ClassVar[str] = "touchable"
    verb: ClassVar[str] = "touch"