# src/twip/extension/pushable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Pushable(MessageAction):
    kind: ClassVar[str] = "pushable"
    verb: ClassVar[str] = "push"