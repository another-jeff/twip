# src/twip/behavior/searchable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Searchable(MessageAction):
    kind: ClassVar[str] = "searchable"
    verb: ClassVar[str] = "search"