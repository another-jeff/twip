from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from twip.entity import Entity


NounPhrase = Callable[["Entity"], str]


class English:
    def room(
        self,
        room: Entity,
        description: str | None,
        contents: list[Entity],
    ) -> str:
        parts = [room.names[-1]]

        if description:
            parts.append(description)

        if contents:
            parts.append(
                "You see "
                f"{self.entity_list(contents, self.indefinite)} "
                "here."
            )

        return "\n".join(parts)

    def not_seen(self, target: str) -> str:
        return f"You don't see {self.indefinite_text(target)} here."

    def look_in_not_container(self, entity: Entity) -> str:
        return f"You can't look inside {self.definite(entity)}."

    def look_in_closed(self, container: Entity) -> str:
        phrase = self.definite(container)
        return f"{self._sentence_start(phrase)} is closed."

    def look_in_empty(self, container: Entity) -> str:
        phrase = self.definite(container)
        return f"{self._sentence_start(phrase)} is empty."

    def look_in_contents(
        self,
        container: Entity,
        contents: list[Entity],
    ) -> str:
        return (
            f"Inside {self.definite(container)}, you see "
            f"{self.entity_list(contents, self.indefinite)}."
        )

    def take_success(
        self,
        item: Entity,
        source: Entity | None,
    ) -> str:
        message = f"You take {self.definite(item)}"

        if source is not None:
            message += f" from {self.definite(source)}"

        return f"{message}."
    
    def take_not_takeable(self, item: Entity) -> str:
        return f"You can't take {self.definite(item)}."

    def not_carried(self, target: str) -> str:
        return (
            "You aren't carrying "
            f"{self.indefinite_text(target)}."
        )

    def put_missing_destination(self, item: Entity) -> str:
        return f"Where do you want to put {self.definite(item)}?"

    def put_unsupported_relation(self, item: Entity) -> str:
        return (
            f"You can't put {self.definite(item)} "
            "there that way."
        )

    def put_in_not_container(self, entity: Entity) -> str:
        return f"You can't put anything in {self.definite(entity)}."

    def put_in_closed(self, container: Entity) -> str:
        phrase = self.definite(container)
        return f"{self._sentence_start(phrase)} is closed."

    def put_in_success(
        self,
        item: Entity,
        container: Entity,
    ) -> str:
        return (
            f"You put {self.definite(item)} "
            f"in {self.definite(container)}."
        )

    def inventory_empty(self) -> str:
        return "You are carrying nothing."

    def inventory_contents(self, items: list[Entity]) -> str:
        return (
            "You are carrying "
            f"{self.entity_list(items, self.indefinite)}."
        )

    def definite(self, entity: Entity) -> str:
        return self.definite_text(entity.name)

    def definite_text(self, text: str) -> str:
        return f"the {text}"

    def indefinite(self, entity: Entity) -> str:
        return self.indefinite_text(entity.name)

    def indefinite_text(self, text: str) -> str:
        article = (
            "an"
            if text[:1].casefold() in "aeiou"
            else "a"
        )
        return f"{article} {text}"

    def entity_list(
        self,
        entities: list[Entity],
        noun_phrase: NounPhrase,
    ) -> str:
        phrases = [
            noun_phrase(entity)
            for entity in sorted(
                entities,
                key=lambda entity: entity.name.casefold(),
            )
        ]

        if not phrases:
            return "nothing"

        if len(phrases) == 1:
            return phrases[0]

        if len(phrases) == 2:
            return f"{phrases[0]} and {phrases[1]}"

        return f"{', '.join(phrases[:-1])}, and {phrases[-1]}"

    def _sentence_start(self, text: str) -> str:
        return text[:1].upper() + text[1:]
    
    def key_does_not_fit(self) -> str:
        return "That key doesn't fit."

    def already_locked(self) -> str:
        return "It's already locked."

    def already_unlocked(self) -> str:
        return "It's already unlocked."

    def lock_success(self) -> str:
        return "Locked."

    def unlock_success(self) -> str:
        return "Unlocked."
    
    def already_open(self, entity: Entity) -> str:
        return f"{self._sentence_start(self.definite(entity))} is already open."

    def already_closed(self, entity: Entity) -> str:
        return f"{self._sentence_start(self.definite(entity))} is already closed."

    def locked(self, entity: Entity) -> str:
        return f"{self._sentence_start(self.definite(entity))} is locked."

    def open_success(self, entity: Entity) -> str:
        return f"You open {self.definite(entity)}."

    def close_success(self, entity: Entity) -> str:
        return f"You close {self.definite(entity)}."
    
    def already_on(self, entity: Entity) -> str:
        return (
            f"{self._sentence_start(self.definite(entity))} "
            "is already on."
        )

    def already_off(self, entity: Entity) -> str:
        return (
            f"{self._sentence_start(self.definite(entity))} "
            "is already off."
        )

    def turn_on_success(self, entity: Entity) -> str:
        return f"You turn on {self.definite(entity)}."

    def turn_off_success(self, entity: Entity) -> str:
        return f"You turn off {self.definite(entity)}."
    
    def movement_not_possible(self) -> str:
        return "You can't go that way."

    def movement_ambiguous(self, target: str) -> str:
        return f"Which {target} way do you mean?"

    def movement_blocked(self) -> str:
        return "It's closed."

    def movement_success(self, direction: str) -> str:
        return f"You go {direction}."
    
    def ambiguous(self, target: str) -> str:
        return f"Which {target}?"

    def drop_success(self, item: Entity) -> str:
        return f"You drop {self.definite(item)}."
    
    def wait_success(self) -> str:
        return "Time passes."