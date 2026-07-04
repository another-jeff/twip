from __future__ import annotations

from dataclasses import dataclass, field
from typing import Self

from twip.action import Action
from twip.component import Component
from twip.result import Result


@dataclass
class Entity:
    names: tuple[str, ...]
    traits: set[str] = field(default_factory=set)
    components: dict[str, Component] = field(default_factory=dict)
    _id: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.names:
            raise ValueError("Entity must have at least one name.")

    @property
    def id(self) -> str:
        if self._id is None:
            raise ValueError("Entity has not been added to a world.")

        return self._id

    @property
    def has_id(self) -> bool:
        return self._id is not None

    @property
    def name(self) -> str:
        return self.names[0]

    def _assign_id(self, id: str) -> None:
        if self._id is not None:
            raise ValueError(f"Entity already has id: {self._id}")

        self._id = id

    def add_component(self, *components: Component) -> Self: 
        for component in components: 
            self.components[component.id] = component 
            
        return self

    def component(self, id: str) -> Component:
        return self.components[id]

    def has_component(self, id: str) -> bool:
        return id in self.components

    def parser_names(self) -> set[str]:
        return {name.lower() for name in self.names}

    def parser_traits(self) -> set[str]:
        return {trait.lower() for trait in self.traits}

    def matches(self, target: str, traits: set[str] | None = None) -> bool:
        words = set(target.lower().split())

        if not words:
            return False

        names = self.parser_names()

        if not words & names:
            return False

        available_traits = self.parser_traits()

        if traits is not None:
            available_traits |= {trait.lower() for trait in traits}

        trait_words = words - names

        return trait_words <= available_traits

    def handle(self, action: Action, world: object) -> Result | None:
        for component in self.components.values():
            result = component.handle(action, self, world)
            if result is not None:
                return result

        return None