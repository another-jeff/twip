# src/twip/extension/drinkable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Drinkable(MessageAction):
    kind: ClassVar[str] = "drinkable"
    verb: ClassVar[str] = "drink"