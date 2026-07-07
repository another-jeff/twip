# src/twip/extension/searchable.py

from __future__ import annotations

from typing import ClassVar

from twip.extension.message_action import MessageAction


class Searchable(MessageAction):
    kind: ClassVar[str] = "searchable"
    verb: ClassVar[str] = "search"