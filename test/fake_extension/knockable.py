# test/fake_extension/knockable.py

from dataclasses import dataclass
from typing import ClassVar

from twip.action import Action
from twip.behavior import Behavior
from twip.result import Result
from twip.verb import register_verb


@dataclass
class Knockable(Behavior):
    kind: ClassVar[str] = "knockable"

    def handle(self, action: Action, entity, world) -> Result | None:
        if action.verb != "knock":
            return None

        return Result.success("You knock on it.")


def register() -> None:
    register_verb("knock")