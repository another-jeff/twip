from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from twip.action import Action
from twip.behavior.base import Behavior
from twip.result import Result
from twip.verb import register_verb

if TYPE_CHECKING:
    from twip.entity import Entity
    from twip.world import World


@dataclass
class VerbMessageBehavior(Behavior):
    message: str

    verb: ClassVar[str]

    @classmethod
    def register_verb(cls) -> None:
        register_verb(cls.verb)

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != self.verb:
            return None

        return Result.success(self.message)