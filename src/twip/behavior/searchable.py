# src/twip/behavior/searchable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Searchable(VerbMessageBehavior):
    kind: ClassVar[str] = "searchable"
    verb: ClassVar[str] = "search"