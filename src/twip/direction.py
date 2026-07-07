# src/twip/direction.py

from __future__ import annotations

N = "north"
S = "south"
E = "east"
W = "west"

NE = "northeast"
SE = "southeast"
NW = "northwest"
SW = "southwest"

U = "up"
D = "down"

IN = "in"
OUT = "out"

ALL = frozenset(
    {
        N,
        S,
        E,
        W,
        NE,
        SE,
        NW,
        SW,
        U,
        D,
        IN,
        OUT,
    }
)

ALIASES = {
    "n": N,
    "north": N,
    "s": S,
    "south": S,
    "e": E,
    "east": E,
    "w": W,
    "west": W,
    "ne": NE,
    "northeast": NE,
    "se": SE,
    "southeast": SE,
    "nw": NW,
    "northwest": NW,
    "sw": SW,
    "southwest": SW,
    "u": U,
    "up": U,
    "d": D,
    "down": D,
    "in": IN,
    "out": OUT,
}


def normalize(value: str | None) -> str | None:
    if value is None:
        return None

    return ALIASES.get(value)


def is_direction(value: str | None) -> bool:
    return normalize(value) is not None