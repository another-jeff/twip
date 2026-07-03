# Behavior Composition

Twip models world objects as entities composed from reusable behavior components.

```text
Entity = thing
Component = behavior
Preset = packaged thing
```

Example:

```text
door_wooden
  Openable

door_wooden_locked
  Openable
  Lockable
```

A component owns its own state and behavior.

```text
Openable owns open / closed state.
Lockable owns locked / unlocked state.
```

When behaviors interact, the attempted behavior decides whether another behavior blocks it.

Example:

```text
Openable checks Lockable before opening.
Lockable does not need to know about Openable.
```

This keeps behavior dependencies directional and local:

```text
open door -> Openable handles the action
open locked door -> Openable sees Lockable is locked and fails cleanly
```

The world state remains the source of truth. Parser text does not imply behavior. Entities and components determine what can actually happen.
