# Twip

Twip is a parser-first deterministic world simulation engine for Python.

It is intended for interactive fiction, text adventures, simulations, experiments, and other systems where typed player commands affect a persistent world.

The world model comes first. The parser is intentionally small. AI may eventually assist when ordinary parsing fails, but deterministic behavior is the foundation.

## Current status

Twip is pre-alpha.

The first milestone is deliberately tiny:

* one `World`
* one `Entity`
* one `Component`
* one `Action`
* one `Result`
* one extension: `door`
* one preset: `door_wooden`
* one parser command: `open door`
* one regression test

If this slice works end-to-end, every later feature can follow the same pattern.

## Design goals

Twip favors:

* deterministic world state
* small composable behavior units
* parser-first command handling
* regression tests for discovered behavior
* reusable extensions
* preset entities for world building
* boring, inspectable Python objects

Twip avoids:

* hidden magic
* world state stored only in text
* AI as the primary interpreter
* over-abstracting before behavior exists

## Core model

At the smallest useful scale:

```text
World owns Entity
Entity owns Component
Component exposes state and capability
Action applies a rule
Result describes what happened
Parser maps text input to an Action
Extension packages reusable behavior
Preset packages ready-made entities
```

Example target behavior:

```text
Input:
  open door

World:
  one room
  one entity: door_wooden
  one component: Door

Expected result:
  the door changes from closed to open
  the player receives a result message
```

Repeated input should also be deterministic:

```text
Input:
  open door

When:
  the wooden door is already open

Expected result:
  the world state does not change
  the player receives a consistent result message
```

## Project layout

```text
twip/
  pyproject.toml
  README.md
  doc/
    decided/
      style.md
      milestone_0.md
  src/
    twip/
      __init__.py
      world.py
      entity.py
      component.py
      action.py
      result.py
      parser.py
      extension/
        __init__.py
        door.py
      preset/
        __init__.py
        door_wooden.py
  test/
    test_open_door.py
```

## Naming conventions

Class names should be singular and should represent one clear concept.

Good:

```text
World
Entity
Component
Action
Result
Door
```

Folder names should be singular.

Good:

```text
extension/
preset/
test/
```

Entity preset names should put the general category first and the variant after it.

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

The exception to the singular rule is ordinary iteration naming:

```python
for item in items:
    ...
```

## Development

Install `pytest` if needed:
```bash
py -m pip install pytest
```

Install in editable mode:

```bash
pip install -e .
```

Run tests:

```bash
py -m pytest
```

## Milestone 0

The first complete behavior should support this regression:

```python
def test_open_closed_wooden_door():
    world = make_world_with_wooden_door()

    result = world.handle("open door")

    assert result.succeeded
    assert world.entity("door_wooden").component("door").is_open
```

A second regression should cover repeating the command:

```python
def test_open_already_open_wooden_door():
    world = make_world_with_open_wooden_door()

    result = world.handle("open door")

    assert result.succeeded
    assert world.entity("door_wooden").component("door").is_open
```

The exact API may change. The invariant should not:

> World state is the source of truth.
