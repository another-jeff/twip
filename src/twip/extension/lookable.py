# src/twip/extension/lookable.py

from __future__ import annotations

from dataclasses import dataclass

from twip.component import Component


@dataclass
class Lookable(Component):
    text: str
    id: str = "lookable"