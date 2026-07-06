# test/test_world_extension_dispatch.py

from twip.action import Action
from twip.component import Component
from twip.entity import Entity
from twip.extension import Containable, Container
from twip.result import Result
from twip.world import World


class Searchable(Component):
    id = "searchable"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "search":
            return None

        return Result.success("You find a brass key.")
    
    
class Diggable(Component):
    id = "diggable"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "dig":
            return None

        if action.preposition != "in":
            return None

        return Result.success("You dig in the dirt and find nothing.")


class UnlockableWith(Component):
    id = "unlockable_with"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "unlock":
            return None

        if action.preposition != "with":
            return None

        if action.indirect_target != "key":
            return Result.failure("That doesn't fit the lock.")

        return Result.success("You unlock the door with the key.")
    
    
class Listenable(Component):
    id = "listenable"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "listen":
            return None

        if action.target:
            return None

        return Result.success("You hear water dripping somewhere nearby.")


class Jumping(Component):
    id = "jumping"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "jump":
            return None

        if action.target:
            return None

        return Result.success("You jump on the spot.")
    

class Edible(Component):
    id = "edible"

    def handle(self, action: Action, entity: Entity, world: World) -> Result | None:
        if action.verb != "eat":
            return None

        return Result.success("You eat the apple.")


def test_extension_component_can_claim_uniform_zebra_verb():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    box = world.add(
        names=("box",),
        traits=set(),
        components=(
            Searchable(),
            Containable(),
        ),
    )

    room.components["container"].items.add(box.id)
    box.components["containable"].parent = room.id
    world.current = room.id

    result = world.handle("search box")

    assert result.ok
    assert result.message == "You find a brass key."
    
    
def test_extension_component_can_claim_prepositional_uniform_zebra_verb():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    dirt = world.add(
        names=("dirt",),
        traits=set(),
        components=(
            Diggable(),
            Containable(),
        ),
    )

    room.components["container"].items.add(dirt.id)
    dirt.components["containable"].parent = room.id
    world.current = room.id

    result = world.handle("dig in dirt")

    assert result.ok
    assert result.message == "You dig in the dirt and find nothing."
    
    
def test_extension_component_can_claim_indirect_target_phrase():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    door = world.add(
        names=("door",),
        traits=set(),
        components=(
            UnlockableWith(),
            Containable(),
        ),
    )

    key = world.add(
        names=("key",),
        traits=set(),
        components=(Containable(),),
    )

    room.components["container"].items.update({door.id, key.id})
    door.components["containable"].parent = room.id
    key.components["containable"].parent = room.id
    world.current = room.id

    result = world.handle("unlock door with key")

    assert result.ok
    assert result.message == "You unlock the door with the key."
    
    
def test_current_room_component_can_claim_targetless_action():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(
            Container(),
            Listenable(),
        ),
    )

    world.current = room.id

    result = world.handle("listen")

    assert result.ok
    assert result.message == "You hear water dripping somewhere nearby."
    
    
def test_player_component_can_claim_targetless_action():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    player = world.add(
        names=("player",),
        traits={"player"},
        components=(
            Container(),
            Jumping(),
        ),
    )

    world.current = room.id
    world.player_id = player.id

    result = world.handle("jump")

    assert result.ok
    assert result.message == "You jump on the spot."
    
    
def test_extension_component_can_claim_action_on_inventory_item():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    player = world.add(
        names=("player",),
        traits={"player"},
        components=(Container(),),
    )

    apple = world.add(
        names=("apple",),
        traits=set(),
        components=(
            Containable(),
            Edible(),
        ),
    )

    world.contain(player, apple)
    world.current = room.id
    world.player_id = player.id

    result = world.handle("eat apple")

    assert result.ok
    assert result.message == "You eat the apple."
    
    
def test_extension_action_is_ambiguous_between_room_and_inventory_items():
    world = World()

    room = world.add(
        names=("room",),
        traits={"room"},
        components=(Container(),),
    )

    player = world.add(
        names=("player",),
        traits={"player"},
        components=(Container(),),
    )

    room_apple = world.add(
        names=("apple",),
        traits=set(),
        components=(
            Containable(),
            Edible(),
        ),
    )

    inventory_apple = world.add(
        names=("apple",),
        traits=set(),
        components=(
            Containable(),
            Edible(),
        ),
    )

    world.contain(room, room_apple)
    world.contain(player, inventory_apple)

    world.current = room.id
    world.player_id = player.id

    result = world.handle("eat apple")

    assert not result.ok
    assert result.message == "Which apple do you mean?"