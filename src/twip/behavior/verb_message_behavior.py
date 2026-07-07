from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.behavior.base import Behavior
from twip.entity import Entity
from twip.result import Result
from twip.verb import register_verb


@dataclass
class VerbMessageBehavior(Behavior):
    message: str

    verb: ClassVar[str]

    @classmethod
    def register_verb(cls) -> None:
        register_verb(cls.verb)

    def handle(self, action: Action, entity: Entity, world: object) -> Result | None:
        if action.verb != self.verb:
            return None

        return Result.success(self.message)