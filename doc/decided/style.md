# Style Decisions

This document records settled style decisions for Twip.

## Naming

Class names must be singular.

Good:

```text
World
Entity
Component
Action
Result
Door
```

Avoid plural class names for concepts that represent one thing.

Good:

```python
class Entity:
    ...
```

Avoid:

```python
class Entities:
    ...
```

## Folder names

Folder names should be singular.

Good:

```text
extension/
preset/
test/
```

Avoid:

```text
extensions/
presets/
tests/
```

The main exception to the singular rule is ordinary iteration naming inside code:

```python
for item in items:
    ...
```

## Entity preset names

Preset names should place the general category first and the variant after it.

Good:

```text
door_wooden
door_wooden_locked
```

Avoid:

```text
wooden_door
locked_wooden_door
```

This keeps related world-building presets grouped together.

## Small first

Prefer the smallest end-to-end slice over a broad partial architecture.

A useful slice includes:

```text
World
Entity
Component
Action
Result
extension
preset
parser command
regression test
```

If the slice feels almost too small, it is probably the right size.

## State

World state is the source of truth.

Text output describes what happened, but text output must not be the only place where state exists.

Good:

```python
assert door.is_open
```

Better than relying only on:

```python
assert result.message == "You open the wooden door."
```

## Tests

Every bug should become a regression test before it becomes a fix.

Tests should describe observable behavior and durable state.

Prefer:

```python
result = world.handle("open door")

assert result.succeeded
assert door.is_open
```

Avoid tests that only prove implementation details.
