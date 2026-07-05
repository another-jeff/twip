# Milestone: Connector Movement

Twip now supports movement between rooms through shared connector entities.

Movement is world-level behavior. It updates `World.current`, not entity containment.

## Core behavior

```text
World.current = current room id

go north
  -> finds a visible connector whose current-side traits include north
  -> moves to the connector's opposite side room
  -> updates World.current
```

Supported verbs:

```text
go
move
```

Movement is handled before normal entity action dispatch.

```text
go north
  -> world movement

open north door
  -> entity action
```

## Connector movement model

A connector is one shared entity relating rooms/spaces.

```text
room_1 -- door -- room_2
```

The door is not copied into each room.

Shared connector state lives on the connector entity.

Side-local movement language lives on `ConnectorSide`.

Example:

```text
room_1 side:
  north door

room_2 side:
  south door
```

From `room_1`:

```text
go north
  -> moves to room_2

go south
  -> fails
```

From `room_2`:

```text
go south
  -> moves to room_1

go north
  -> fails
```

## Movement target rules

Movement requires side-local direction language.

Valid:

```text
go north
go north door
go north wooden door
```

Invalid:

```text
go door
go wooden door
```

This keeps movement distinct from ordinary object interaction.

A connector phrase may include connector names and traits, but it must also include a side-local trait from the current room side.

## Ambiguity

Ambiguous movement is a clean failure and must not mutate world state.

Example:

```text
room has two north doors

go north
  -> ambiguous
  -> World.current unchanged
```

Disambiguation uses normal parser-facing connector language plus side-local traits.

```text
go north wooden door
  -> resolves wooden north door
  -> moves through that connector
```

## Blocking movement

Closed connectors block movement.

```text
closed door

go north
  -> fails
  -> World.current unchanged
```

Open connectors permit movement.

```text
open door

go north
  -> succeeds
  -> World.current changes
```

Non-openable connectors are passable for now.

Locked state does not directly block movement.

Instead:

```text
Lockable blocks opening.
Openable blocks movement when closed.
```

So:

```text
locked closed door
  open north door -> fails
  go north        -> fails because closed

unlock north door
open north door
go north
  -> succeeds
```

## Scope composition

Movement composes with containment scope.

After moving rooms:

```text
contents of previous room are no longer visible
contents of new current room are visible
```

Movement updates visibility by changing `World.current`.

Containment does not need to change when the player moves.

## Important design decisions

```text
Movement is world behavior for now.
Connector enables movement.
Openable may block movement.
Lockable blocks opening, not movement directly.
Ambiguous movement does not mutate World.current.
Movement requires side-local direction language.
Connector state remains shared across rooms.
```

## Tests added

```text
go direction moves to connected room
go unknown direction fails cleanly
closed door blocks movement
open door allows movement
movement changes visible room contents
ambiguous movement fails without moving
movement can be disambiguated by connector phrase
closed disambiguated movement still fails
open door then go moves
movement uses other side direction after room changes
locked closed door cannot be opened or moved through
unlock open then go moves through door
go connector without side direction fails without moving
```

## Non-goals

Deferred:

```text
player entity
inventory movement
take / drop
permissions
keys
side-local lock access
room descriptions
look command
automatic room contents listing
multi-side connectors beyond current simple opposite-side movement
```

## Likely next work

```text
Add player/inventory behavior
Add take/drop using Container and Containable
Add look/describe current room
Add room contents listing
Then revisit side-local lock access and key possession
```
