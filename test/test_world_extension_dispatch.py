# test/test_world_extension_dispatch.py

from typing import ClassVar

from twip.action import Action
from twip.behavior import Behavior
from twip.entity import Entity
from twip.behavior import Containable, Container
from twip.result import Result
from twip.world import World

from scenario import bs


class Searchable(Behavior):
    kind: ClassVar[str] = "searchable"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "search":
            return None

        return Result.success("You find a brass key.")


class Diggable(Behavior):
    kind: ClassVar[str] = "diggable"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "dig":
            return None

        if action.preposition != "in":
            return None

        return Result.success("You dig in the dirt and find nothing.")


class UnlockableWith(Behavior):
    kind: ClassVar[str] = "unlockable_with"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "unlock":
            return None

        if action.preposition != "with":
            return None

        if action.target_indirect != "key":
            return Result.failure("That doesn't fit the lock.")

        return Result.success("You unlock the door with the key.")


class Listenable(Behavior):
    kind: ClassVar[str] = "listenable"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "listen":
            return None

        if action.target:
            return None

        return Result.success("You hear water dripping somewhere nearby.")


class Jumping(Behavior):
    kind: ClassVar[str] = "jumping"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "jump":
            return None

        if action.target:
            return None

        return Result.success("You jump on the spot.")


class Edible(Behavior):
    kind: ClassVar[str] = "edible"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "eat":
            return None

        return Result.success("You eat the apple.")


def scenario():
    return bs().one_room()


def player_scenario():
    s = scenario()

    player = s.world.add(
        names=("player",),
        traits={"player"},
        behaviors=(Container(),),
    )

    s.player = player
    s.world.player_id = player.id

    return s


def room_item(s, name: str, *behaviors: Behavior) -> Entity:
    entity = s.world.add(
        names=(name,),
        traits=set(),
        behaviors=(
            *behaviors,
            Containable(),
        ),
    )

    s.world.contain(s.room_one, entity)

    return entity


def inventory_item(s, name: str, *behaviors: Behavior) -> Entity:
    entity = s.world.add(
        names=(name,),
        traits=set(),
        behaviors=(
            *behaviors,
            Containable(),
        ),
    )

    s.world.contain(s.player, entity)

    return entity


def test_extension_behavior_can_claim_uniform_zebra_verb():
    s = scenario()
    room_item(s, "box", Searchable())

    result = s.handle("search box")

    assert result.ok
    assert result.message == "You find a brass key."


def test_extension_behavior_can_claim_prepositional_uniform_zebra_verb():
    s = scenario()
    room_item(s, "dirt", Diggable())

    result = s.handle("dig in dirt")

    assert result.ok
    assert result.message == "You dig in the dirt and find nothing."


def test_extension_behavior_can_claim_target_indirect_phrase():
    s = scenario()
    room_item(s, "door", UnlockableWith())
    room_item(s, "key")

    result = s.handle("unlock door with key")

    assert result.ok
    assert result.message == "You unlock the door with the key."


def test_current_room_behavior_can_claim_targetless_action():
    s = scenario()
    s.room_one.add_behavior(Listenable())

    result = s.handle("listen")

    assert result.ok
    assert result.message == "You hear water dripping somewhere nearby."


def test_player_behavior_can_claim_targetless_action():
    s = player_scenario()
    s.player.add_behavior(Jumping())

    result = s.handle("jump")

    assert result.ok
    assert result.message == "You jump on the spot."


def test_extension_behavior_can_claim_action_on_inventory_item():
    s = player_scenario()
    inventory_item(s, "apple", Edible())

    result = s.handle("eat apple")

    assert result.ok
    assert result.message == "You eat the apple."


def test_extension_action_is_ambiguous_between_room_and_inventory_items():
    s = player_scenario()

    room_item(s, "apple", Edible())
    inventory_item(s, "apple", Edible())

    result = s.handle("eat apple")

    assert not result.ok
    assert result.message == "Which apple do you mean?"