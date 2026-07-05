from __future__ import annotations

from dataclasses import dataclass, field

from twip.component import Component
from twip.entity import Entity
from twip.extension import Containable, Container, Connector, Openable, OpenState, Lookable
from twip.parser import Parser
from twip.result import Result


Connection = tuple[Entity | str, str | set[str]]


@dataclass
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    parser: Parser = field(default_factory=Parser)
    current: str | None = None
    player_id: str | None = None
    _next_entity_id: int = 1

    def add(
        self,
        names: tuple[str, ...],
        traits: set[str] | None = None,
        components: tuple[Component, ...] = (),
    ) -> Entity:
        entity = Entity(
            names=names,
            traits=traits or set(),
        )

        entity.add_component(*components)

        return self._add_entity(entity)

    def add_and_connect(
        self,
        names: tuple[str, ...],
        connections: tuple[Connection, ...],
        traits: set[str] | None = None,
        components: tuple[Component, ...] = (),
    ) -> Entity:
        connector = Connector.from_connections(connections)

        return self.add(
            names=names,
            traits=traits,
            components=(*components, connector),
        )

    def _add_entity(self, entity: Entity) -> Entity:
        if entity.has_id:
            raise ValueError(f"Entity already has id: {entity.id}")

        id = self._next_id()
        entity._assign_id(id)
        self.entities[id] = entity

        return entity

    def _next_id(self) -> str:
        id = f"entity_{self._next_entity_id}"
        self._next_entity_id += 1
        return id

    def entity(self, id: str) -> Entity:
        return self.entities[id]
    
    def handle(self, text: str) -> Result:
        action = self.parser.parse(text)

        if not action.verb:
            return Result.failure("Nothing happens.")

        if action.verb == "inventory":
            return self._inventory()

        if action.verb == "look":
            return self._look()

        if not action.target:
            return Result.failure(f"{action.verb.capitalize()} what?")
        
        if action.verb == "take":
            return self._take(action.target)
        
        if action.verb == "drop":
            return self._drop(action.target)

        if action.verb in {"go", "move"}:
            return self._move(action.target)

        matching_entities = self.find_all(action.target)

        if not matching_entities:
            return Result.failure(f"You don't see {action.target} here.")

        if len(matching_entities) > 1:
            return Result.failure(f"Which {action.target} do you mean?")

        entity = matching_entities[0]

        result = entity.handle(action, self)

        if result is None:
            return Result.failure("You can't do that.")

        return result

    def _move(self, target: str) -> Result:
        if self.current is None:
            return Result.failure("You can't go that way.")

        exits = self._matching_exits(target)

        if not exits:
            return Result.failure("You can't go that way.")

        if len(exits) > 1:
            return Result.failure(f"Which {target} way do you mean?")

        entity, connector = exits[0]

        if self._connector_blocks_movement(entity):
            return Result.failure("It's closed.")

        there = self._other_side(connector, self.current)

        if there is None:
            return Result.failure("You can't go that way.")

        self.current = there.room
        
        return Result.success("You go that way.")

    def _matching_exits(self, target: str) -> list[tuple[Entity, Connector]]:
        exits = []

        for entity in self.entities.values():
            connector = entity.components.get(Connector.id)

            if not isinstance(connector, Connector):
                continue

            here = connector.side_for(self.current)

            if here is None:
                continue

            if target in here.traits:
                exits.append((entity, connector))
                continue

            if not self._target_mentions_side(target, here.traits):
                continue

            if entity.matches(target, traits=here.traits):
                exits.append((entity, connector))

        return exits

    def _target_mentions_side(self, target: str, side_traits: set[str]) -> bool:
        words = set(target.split())

        return bool(words & side_traits)

    def _other_side(self, connector: Connector, room_id: str):
        for side in connector.sides:
            if side.room != room_id:
                return side

        return None

    def find(self, target: str) -> Entity | None:
        matching_entities = self.find_all(target)

        if len(matching_entities) == 1:
            return matching_entities[0]

        return None

    def find_all(self, target: str) -> list[Entity]:
        return [
            entity
            for entity in self.entities.values()
            if self._is_visible(entity)
            if self._matches(entity, target)
        ]

    def _matches(self, entity: Entity, target: str) -> bool:
        if self.current is None:
            return entity.matches(target)

        if not entity.has_component(Connector.id):
            return entity.matches(target)

        connector = entity.component(Connector.id)

        if not isinstance(connector, Connector):
            return False

        side = connector.side_for(self.current)

        if side is None:
            return False

        return entity.matches(target, traits=side.traits)
    
    def _is_visible(self, entity: Entity) -> bool:
        if self.current is None:
            return True

        if entity.id == self.current:
            return True

        if Connector.id in entity.components:
            return self._connector_is_visible(entity)

        containable = entity.components.get(Containable.id)

        return (
            containable is not None
            and containable.parent == self.current
        )


    def _connector_is_visible(self, entity: Entity) -> bool:
        connector = entity.component(Connector.id)

        if not isinstance(connector, Connector):
            return False

        return connector.side_for(self.current) is not None


    def contain(self, container: Entity, entity: Entity) -> None:
        container.components[Container.id].items.add(entity.id)
        entity.components[Containable.id].parent = container.id
        
    def _connector_blocks_movement(self, entity: Entity) -> bool:
        openable = entity.components.get(Openable.id)

        return (
            isinstance(openable, Openable)
            and openable.state == OpenState.CLOSED
        )
        
    def _take(self, target: str) -> Result:
        if not self.player_id:
            return Result.failure("There is no player.")

        player = self.entities[self.player_id]
        player_container = player.component("container")

        matching_entities = self.find_all(target)

        if not matching_entities:
            return Result.failure(f"You don't see {target} here.")

        if len(matching_entities) > 1:
            return Result.failure(f"Which {target}?")

        entity = matching_entities[0]

        if "containable" not in entity.components:
            return Result.failure(f"You can't take {target}.")

        containable = entity.component("containable")

        if containable.parent:
            parent = self.entities[containable.parent]
            parent_container = parent.component("container")
            parent_container.items.remove(entity.id)

        player_container.items.add(entity.id)
        containable.parent = player.id

        return Result.success(f"Taken.")
        
    def _drop(self, target: str) -> Result:
        if not self.player_id:
            return Result.failure("There is no player.")

        if not self.current:
            return Result.failure("You are nowhere.")

        player = self.entities[self.player_id]
        room = self.entities[self.current]

        player_container = player.component("container")
        room_container = room.component("container")

        matching_entities = [
            self.entities[item_id]
            for item_id in player_container.items
            if self._matches(self.entities[item_id], target)
        ]

        if not matching_entities:
            return Result.failure(f"You aren't carrying {target}.")

        if len(matching_entities) > 1:
            return Result.failure(f"Which {target}?")

        entity = matching_entities[0]
        containable = entity.component("containable")

        player_container.items.remove(entity.id)
        room_container.items.add(entity.id)
        containable.parent = room.id

        return Result.success("Dropped.")
    
    def _inventory(self) -> Result:
        if not self.player_id:
            return Result.failure("There is no player.")

        player = self.entities[self.player_id]
        container = player.component(Container.id)

        if not container.items:
            return Result.success("You are carrying nothing.")

        names = sorted(
            self.entities[item_id].names[0]
            for item_id in container.items
        )

        return Result.success("You are carrying: " + ", ".join(names))
    
    def _look(self) -> Result:
        if not self.current:
            return Result.failure("You are nowhere.")

        room = self.entities[self.current]
        message = f"You are in {room.names[-1]}."

        lookable = room.components.get("lookable")

        if lookable:
            message += f" {lookable.text}"

        container = room.components.get("container")

        if container and container.items:
            names = sorted(
                self.entities[item_id].names[0]
                for item_id in container.items
            )
            message += f" You see {', '.join(names)} here."

        return Result.success(message)
    
    