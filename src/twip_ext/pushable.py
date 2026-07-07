# src/twip_ext/pushable.py

from twip.behavior import VerbMessageBehavior


class Pushable(VerbMessageBehavior):
    kind = "pushable"
    verb = "push"


def register() -> None:
    Pushable.register_verb()