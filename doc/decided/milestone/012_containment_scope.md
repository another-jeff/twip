# Milestone 012: Structural Containment and Scope

Status:
All tests green.

## Direction

Containment is world structure.

An entity's `parent` is the single source of truth for where that
entity is located.

`Container` does not store contents. It marks an ordinary entity as
capable of holding other entities and participating in container
commands.

## Structural parents

The following entities may structurally parent other entities:

- rooms registered through `World.add_room()`
- the entity identified by `World.player_id`
- ordinary entities with `Container`

Rooms and the player do not require `Container`.

This keeps two concepts separate:

- structural parentage
- interactive container behavior

## World.put

`World.put(parent, entity)` places or moves an entity beneath a valid
structural parent.

Examples:

```python
world.put(room, coin)
world.put(player, coin)
world.put(box, coin)
```

`World.put`:

- reparents an already-placed entity
- is idempotent when the entity is already beneath that parent
- rejects ordinary entities that cannot parent contents
- rejects self-containment
- rejects containment cycles
- validates before mutation

Commands convert rejected structural changes into failed `Result`
objects rather than allowing `ValueError` to escape.

## Contents

Contents are derived from entity parentage:

```python
world.contents_of(parent)
```

There is no duplicated `Container.items` collection.

Inventory, room descriptions, `take`, `drop`, `put`, and `look in`
all use structural parentage.

## Container

`Container` is marker behavior:

```python
@dataclass
class Container(Behavior):
    kind: ClassVar[str] = "container"
```

It means:

> This ordinary entity can hold contents and participate in
> container-specific commands.

It does not mean:

- the entity currently contains something
- rooms must carry the behavior
- the player must carry the behavior
- contents are stored on the behavior

## Visibility and reachability

Visibility and reachability are derived from containment paths.

The current room and the player are parallel scope roots.

An entity can therefore be found through:

- the current room
- nested open containers in the current room
- the player's inventory
- nested open containers carried by the player

Every intermediate `Openable` container must be open.

A closed container blocks both visibility and reachability to its
contents.

The closed container itself remains visible and reachable when its
own parent path allows it.

Connectors retain their existing sided visibility rules.

## Takeable

Taking is explicitly behavior-driven.

An entity must have `Takeable` before `take` can move it into the
player's inventory.

Successful taking:

- requires a reachable target
- moves the entity beneath the player
- reports the source container when appropriate

Failed taking does not mutate containment.

An already-carried object is not selected as a new take target.

## Putting

`put X in Y` and `put X into Y` use structural containment.

The direct object:

- must be carried
- must resolve unambiguously

The destination:

- must be reachable
- must resolve unambiguously
- must have `Container`
- must be open when it has `Openable`

Putting a container inside itself or one of its descendants fails
without mutation.

## Looking inside containers

Supported forms:

```text
look in box
look into box
look inside box
```

The parser normalizes `in`, `into`, and `inside` to the canonical
preposition `in`.

`look in`:

- rejects entities without `Container`
- reports closed containers
- reports empty containers
- lists direct contents of open containers
- does not flatten nested contents
- works for containers in the room or carried by the player

## Testing

Coverage now includes:

- rooms parenting entities without `Container`
- player inventory without `Container`
- ordinary containers parenting entities
- invalid structural parents
- reparenting
- self-containment rejection
- containment-cycle rejection
- room and inventory scope roots
- nested open and closed containers
- taking from nested containers
- putting containers into invalid descendants
- direct-content listing through `look in`
- end-to-end prototype containment state

## Deferred

Not included in this milestone:

- transparent closed containers
- supporters and objects placed on other objects
- darkness and light propagation
- distance and physical barriers
- container capacity
- bulk or weight limits
- automatic recursive room-description listing