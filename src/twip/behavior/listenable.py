# src/twip/behavior/listenable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Listenable(MessageAction):
    kind: ClassVar[str] = "listenable"
    verb: ClassVar[str] = "listen"