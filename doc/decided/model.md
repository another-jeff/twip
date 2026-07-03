# Model Decisions

Twip models a world as things with behaviors.

## Core vocabulary

A `World` contains things.

A thing is a world object the player may be able to refer to, examine, manipulate, move through, carry, alter, or otherwise interact with.

A behavior is reusable logic attached to a thing.

Examples:

```text
wooden door
  behaviors:
    Openable

locked wooden door
  behaviors:
    Openable
    Lockable

brass lamp
  behaviors:
    Portable
    Lightable
```

## Current code names

The current implementation uses:

```text
Entity    = thing
Component = behavior
```

These names may be renamed later, but the model decision is already clear:

```text
Thing owns Behavior
```

## Why behaviors instead of object-specific classes

A door is not the behavior.

A door is a thing that may have openable behavior, lockable behavior, passage behavior, breakable behavior, and so on.

This allows behavior to be reused.

Examples:

```text
door      → Openable
box       → Openable
window    → Openable
gate      → Openable
cabinet   → Openable
```

The thing determines identity and presentation.

The behavior determines capability and state.

## Openable

`Openable` represents the ability to be opened and closed.

It owns open/closed state.

It handles actions such as:

```text
open door
close door
```

It should not assume the thing is a door.

## Lockable

`Lockable` represents the ability to be locked and unlocked.

It owns locked/unlocked state.

It may eventually block actions handled by other behaviors.

Example:

```text
open locked door
→ Lockable blocks the action
→ Openable does not open
```

## Design rule

Prefer behavior names that describe capabilities.

Good:

```text
Openable
Lockable
Portable
Readable
Lightable
Container
Supporter
```

Avoid behavior names that describe only one kind of object.

Less reusable:

```text
Door
Box
Window
Lamp
```

Object-specific names belong in presets.

Good:

```text
door_wooden
door_wooden_locked
box_cardboard
lamp_brass
```

## Invariant

World state belongs to things and behaviors, not to parser text or result messages.

The parser interprets input.

Behaviors change world state.

Results report what happened.
