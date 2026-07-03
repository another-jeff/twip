from __future__ import annotations

from dataclasses import dataclass, field

from twip.action import Action
from twip.component import Component
from twip.result import Result


@dataclass
class Entity:
    names: tuple[str, ...]
    traits: set[str] = field(default_factory=set)
    components: dict[str, Component] = field(default_factory=dict)
    _key: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.names:
            raise ValueError("Entity must have at least one name.")

    @property
    def key(self) -> str:
        if self._key is None:
            raise ValueError("Entity has not been added to a world.")

        return self._key

    @property
    def has_key(self) -> bool:
        return self._key is not None

    @property
    def name(self) -> str:
        return self.names[0]

    def _assign_key(self, key: str) -> None:
        if self._key is not None:
            raise ValueError(f"Entity already has key: {self._key}")

        self._key = key

    def add_component(self, component: Component) -> None:
        self.components[component.key] = component

    def component(self, key: str) -> Component:
        return self.components[key]

    def has_component(self, key: str) -> bool:
        return key in self.components

    def parser_names(self) -> set[str]:
        return {name.lower() for name in self.names}

    def parser_traits(self) -> set[str]:
        return {trait.lower() for trait in self.traits}

    def matches(self, target: str) -> bool:
        words = set(target.lower().split())

        if not words:
            return False

        names = self.parser_names()

        if not words & names:
            return False

        trait_words = words - names

        return trait_words <= self.parser_traits()

    def handle(self, action: Action, world: object) -> Result | None:
        for component in self.components.values():
            result = component.handle(action, self, world)
            if result is not None:
                return result

        return None