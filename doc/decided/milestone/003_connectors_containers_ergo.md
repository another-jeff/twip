# Milestone 003: scope and connection groundwork

## Added
  Container
  Containable
  Connector
  ConnectorSide
  side-local connector traits
  current-room connector scope
  authoring ergonomics

## World/entity authoring
```python
  world.add(...)
```

```python
  world.add_and_connect(...)
```

```python
  Entity.add_component(*components)
```

## Parser/world behavior
  connector entities are visible from rooms they touch
  side-local traits match only from the current side
  multiple visible same-name doors are ambiguous
  ambiguity does not mutate world state

## Design decisions
  containment is not connection
  doors are single shared entities between rooms
  rooms contain things
  connectors relate rooms
  inventory remains later