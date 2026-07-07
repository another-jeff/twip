# Twip Extensions

A Twip extension is an importable Python module with a callable `register()` function.

`load_extension()` imports or accepts the module, calls `register()`, and returns the module.

Extensions may register parser verb policy:

```python
from twip.verb import register_verb


def register() -> None:
    register_verb("push")
```

Extensions may provide behaviors:

```python
from twip.behavior import VerbMessageBehavior


class Pushable(VerbMessageBehavior):
    kind = "pushable"
    verb = "push"


def register() -> None:
    Pushable.register_verb()
```

An extension behavior is attached to an entity like any other behavior:

```python
door.add_behavior(Pushable("The button clicks."))
```

The dispatcher does not know concrete extension behaviors.

The dispatcher resolves command shape and target, then asks the target entity to handle the action.

## Behavior handling contract

A behavior handles an action by returning a `Result`.

A behavior ignores an action by returning `None`.

`Result.success(...)` means the behavior claimed the action and handled it successfully.

`Result.failure(...)` means the behavior claimed the action and failed.

Both success and failure stop behavior dispatch.

Later behaviors only run when earlier behaviors return `None`.

## Extension boundary

Core Twip owns:

- parsing text into `Action`
- registered verb policy
- command routing
- world and entity state
- behavior iteration
- extension loading

Extensions may own:

- concrete behavior classes
- verb registration
- action semantics for those behaviors

A concrete extension behavior should not require changes to the parser, dispatcher, world, or entity dispatch loop.