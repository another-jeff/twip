# Scope and Visibility

Parser target lookup should use the actor's current scope.

Scope is what can be referred to from the actor's current room.

Scope is not the same as containment.

## Current room scope

From a room, the parser may resolve targets among:

```text
entities contained by the current room
connector entities touching the current room
```

Example:

```text
Hall contains:
  coin
  table

Hall is connected by:
  north door
```

From the hall, these may be visible parser targets:

```text
coin
table
door
north door
```

The door does not need to be contained by the hall.

It is visible because it touches the hall as a connector.

## Local language

Some parser-facing language is local to the current room.

Example:

```text
same door

from hall:
  north door

from kitchen:
  south door
```

The words `north` and `south` are not global traits of the door.

They are side-local traits.

This is wrong:

```text
door.traits = {"wooden", "north", "south"}
```

That would allow `north door` and `south door` to match from both rooms.

The correct model is:

```text
door.traits = {"wooden"}

hall side:
  traits={"north"}

kitchen side:
  traits={"south"}
```

## Matching rule

Target matching still requires at least one parser-facing name.

Global traits and side-local traits may disambiguate a named target.

Example from hall:

```text
matches:
  door
  wooden door
  north door
  north wooden door

does not match:
  north
  wooden
  south door
```

Example from kitchen:

```text
matches:
  door
  wooden door
  south door
  south wooden door

does not match:
  south
  wooden
  north door
```

## Ambiguity

Ambiguity is normal.

If the current room can see two doors, then:

```text
open door
```

is ambiguous.

If one is locally described as north and the other as south, then:

```text
open north door
```

resolves to only the north-visible door.

Ambiguity must not mutate world state.

## Rule

Scope answers what the parser can see.

Containment answers what is inside what.

Connection answers what joins rooms.
