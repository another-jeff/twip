from __future__ import annotations

from dataclasses import dataclass, field

from twip.action import Action
from twip.component import Component
from twip.result import Result


@dataclass
class Entity:
    key: str
    name: str
    aliases: set[str] = field(default_factory=set)
    components: dict[str, Component] = field(default_factory=dict)

    def add_component(self, component: Component) -> None:
        self.components[component.key] = component

    def component(self, key: str) -> Component:
        return self.components[key]

    def has_component(self, key: str) -> bool:
        return key in self.components

    def matches(self, target: str) -> bool:
        normalized = target.lower()

        return normalized in {
            self.key.lower(),
            self.name.lower(),
            *self.aliases,
        }

    def handle(self, action: Action, world: object) -> Result | None:
        for component in self.components.values():
            result = component.handle(action, self, world)
            if result is not None:
                return result

        return None