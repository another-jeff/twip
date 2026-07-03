# Milestone 2: Initial Behavior Composition

Twip now supports its first meaningful composed behavior.

The initial end-to-end loop is working:

```text
text input
  -> Parser
  -> Action
  -> World target lookup
  -> Entity
  -> Component behavior
  -> Result
  -> World state mutation
```

The first composed preset is:

```text
door_wooden_locked
  Openable
  Lockable
```

The supported command set now includes:

```text
open door
close door
lock door
unlock door
```

Behavior composition is confirmed by the locked-door rule:

```text
open locked door -> fails cleanly
unlock door -> succeeds
open door -> succeeds
```

This milestone establishes the core Twip direction:

```text
Entity = thing
Component = behavior
Preset = packaged thing composed from behaviors
World state = source of truth
```

This is the first point where Twip is more than a single behavior demo. It now demonstrates deterministic world simulation through reusable, composable behaviors.
