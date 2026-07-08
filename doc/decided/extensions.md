# Twip Extensions

A Twip extension is an importable Python module with a callable `register()` function.

`load_extension()` imports or accepts the module, calls `register()`, and returns the module.

## Package shape

Core Twip lives in the `twip` package.

External extension packages should use the `twipx-*` distribution naming pattern:

```text
twip
twipx-viewing
twipx-breaking
twipx-wearing
```

Extension imports should use the `twipx.[concern]` namespace pattern:

```python
from twipx.viewing import LookThroughable, ViewingCovered
```

For example:

```text
twipx-viewing/
  pyproject.toml
  src/
    twipx/
      viewing/
        __init__.py
        look_throughable.py
        viewing_covered.py
  test/
```

The top-level `twipx` package should be a namespace package.

Do not add:

```text
src/twipx/__init__.py
```

This allows multiple independently installed extension packages to share the `twipx` namespace.

## Loading extensions

Extensions are loaded by import path:

```python
from twip.extensions import load_extension

load_extension("twipx.viewing")
```

The extension module must provide `register()`:

```python
def register() -> None:
    pass
```

## Verb registration

Extensions may register parser verb policy:

```python
from twip.verb import register_verb


def register() -> None:
    register_verb("push")
```

Extensions may also provide behaviors that register their own verbs:

```python
from twip.behavior import VerbMessageBehavior


class Pushable(VerbMessageBehavior):
    kind = "pushable"
    verb = "push"


def register() -> None:
    Pushable.register_verb()
```

## Behaviors

Extensions may provide concrete behavior classes.

An extension behavior is attached to an entity like any other behavior:

```python
door.add_behavior(Pushable("The button clicks."))
```

For example, `twipx-viewing` owns viewing behaviors:

```python
from twipx.viewing import LookThroughable, ViewingCovered
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

## Extension interaction

Extension behaviors may interact with other behaviors, but should avoid hard dependencies when possible.

Prefer interaction through stable behavior shape:

```python
behavior = entity.behaviors.get("breakable")

if getattr(behavior, "broken", False):
    ...
```

This allows one extension to respond to another extension’s behavior without importing it directly.

Hard imports between extensions are allowed only when the dependency is intentional and should be declared as a package dependency.

## Extension boundary

Core Twip owns:

* parsing text into `Action`
* registered verb policy
* command routing
* world and entity state
* behavior iteration
* extension loading

Extensions may own:

* concrete behavior classes
* verb registration
* action semantics for those behaviors
* interaction between related behaviors

A concrete extension behavior should not require changes to the parser, dispatcher, world, or entity dispatch loop.

## Reference extension

`twipx-viewing` is the first reference extension.

It proves:

* external packages can depend on `twip`
* extensions can import as `twipx.[concern]`
* extensions can load through `load_extension(...)`
* concrete behaviors can live outside core
* extension behaviors can interact without parser or dispatcher changes
