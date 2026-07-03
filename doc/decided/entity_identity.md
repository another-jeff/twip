# Entity Identity and Parser Names

Entity identity is not language.

An entity has a unique internal identity. Parser-facing names, nouns, aliases, and descriptors are not unique.

```text
Entity id = stable internal identity
Parser name = language used to refer to the entity
Preset name = reusable construction recipe
```

These are different things.

```text
preset: door_wooden
entity id: north_door
parser noun: door
descriptor: north
```

Multiple entities may share the same parser noun.

```text
north_door
  noun: door
  descriptor: north

south_door
  noun: door
  descriptor: south
```

The parser must not assume that a noun resolves to one entity.

Target lookup returns one of three outcomes:

```text
none
one
many
```

Examples:

```text
open door
  -> matches north_door and south_door
  -> ambiguous

open north door
  -> matches north_door
  -> resolved

open trapdoor
  -> matches nothing
  -> missing target
```

Ambiguity is a normal result, not an exception.

```text
Which door do you mean?
```

The world state is the source of truth for which entities are currently in scope.

A room is not special at the identity level. A room is an entity that can contain other entities.

```text
bedroom
  Container

north_door
  Openable
  noun: door
  descriptor: north

south_door
  Openable
  noun: door
  descriptor: south
```

A room does not need to be containable.

A door in a room does not need to be containable until the engine supports moving doors between containers.

The first purpose of room containment is parser scope:

```text
Only entities in the current room are parser candidates.
```

Rules decided:

```text
Entity ids must be unique.
Parser names do not need to be unique.
Preset names do not become entity ids automatically.
Target lookup returns candidates.
Many candidates produce an ambiguous Result.
Ambiguity does not mutate world state.
```
