# src/twip/extension/listenable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Listenable(MessageAction):
    kind: ClassVar[str] = "listenable"
    verb: ClassVar[str] = "listen"