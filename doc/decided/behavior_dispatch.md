# Behavior Dispatch

Behaviors are entity-attached capabilities.

A behavior handles an action by returning a Result.
A behavior ignores an action by returning None.

Result.success and Result.failure both mean the behavior claimed the action.
Later behaviors are only consulted when earlier behaviors return None.

The dispatcher does not know concrete behaviors such as Pushable.
The dispatcher resolves action shape and target, then asks the entity to handle the action.