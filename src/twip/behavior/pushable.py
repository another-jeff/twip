# src/twip/behavior/pushable.py

from twip.behavior.verb_message_behavior import VerbMessageBehavior
from twip.verb import register_verb


class Pushable(VerbMessageBehavior):
    kind = "pushable"
    verb = "push"


def register() -> None:
    register_verb("push")