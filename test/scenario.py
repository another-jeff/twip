from dataclasses import dataclass
from typing import Callable

from twip import direction
from twip.component import Component
from twip.entity import Entity
from twip.world import World

from helpers import described_room, player as make_player

import tt


EntityFactory = Callable[[World], Entity]


@dataclass
class BasicScenario:
    world: World
    room_one: Entity | None = None
    room_two: Entity | None = None
    room_three: Entity | None = None
    player: Entity | None = None

    def handle(self, text: str):
        return self.world.handle(text)

    def one_room(self):
        self.room_one = described_room(self.world, tt.ROOM_1)
        self.world.current = self.room_one.id
        return self

    def two_rooms(self):
        self.one_room()
        self.room_two = described_room(self.world, tt.ROOM_2)
        return self

    def three_rooms(self):
        self.two_rooms()
        self.room_three = described_room(self.world, tt.ROOM_3)
        return self

    def with_player(self):
        self.player = make_player(self.world)
        self.world.player_id = self.player.id
        return self

    def put_room(self, room: Entity, *factories: EntityFactory):
        entities = [factory(self.world) for factory in factories]

        for entity in entities:
            self.world.contain(room, entity)

        return one_or_many(entities)

    def put_inventory(self, *factories: EntityFactory):
        if self.player is None:
            self.with_player()

        entities = [factory(self.world) for factory in factories]

        for entity in entities:
            self.world.contain(self.player, entity)

        return one_or_many(entities)

    def connect(
        self,
        room: Entity | None = None,
        *,
        traits: set[str] | None = None,
        components: tuple[Component, ...] = (),
    ) -> Entity:
        return self.world.add_and_connect(
            names=(tt.DOOR,),
            connections=(
                (self.room_one, direction.N),
                (room or self.room_two, direction.S),
            ),
            traits=traits,
            components=components,
        )


def bs() -> BasicScenario:
    return BasicScenario(World())


def one_or_many(entities: list[Entity]):
    if len(entities) == 1:
        return entities[0]

    return entities