from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from twip.component import Component
from twip.entity import Entity


class LockAccessKind(Enum):
    FREE = "free"
    KEYED = "keyed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class LockAccess:
    kind: LockAccessKind = LockAccessKind.FREE

    @property
    def can_lock(self) -> bool:
        return self.kind != LockAccessKind.BLOCKED

    @property
    def can_unlock(self) -> bool:
        return self.kind != LockAccessKind.BLOCKED

    @property
    def needs_key(self) -> bool:
        return self.kind == LockAccessKind.KEYED


@dataclass(frozen=True)
class ConnectorSide:
    room: str
    traits: set[str]
    lock_access: LockAccess | None = None


@dataclass
class Connector(Component):
    kind: ClassVar[str] = "connector"

    sides: tuple[ConnectorSide, ...]

    def side_for(self, room: str) -> ConnectorSide | None:
        for side in self.sides:
            if side.room == room:
                return side
        return None

    def touches(self, room: str) -> bool:
        return self.side_for(room) is not None

    def other_side(self, room: str) -> ConnectorSide | None:
        if not self.touches(room):
            return None

        others = [side for side in self.sides if side.room != room]
        if len(others) != 1:
            return None

        return others[0]
    
    @classmethod
    def from_connections(
        cls,
        connections: tuple[tuple[Entity | str, str | set[str]], ...],
    ) -> "Connector":
        return cls(
            sides=tuple(
                ConnectorSide(
                    room=room.id if isinstance(room, Entity) else room,
                    traits={traits} if isinstance(traits, str) else traits,
                )
                for room, traits in connections
            )
        )