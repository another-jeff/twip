# src/twip/behavior/pullable.py

from __future__ import annotations

from typing import ClassVar

from twip.behavior.message_action import MessageAction


class Pullable(MessageAction):
    kind: ClassVar[str] = "pullable"
    verb: ClassVar[str] = "pull"