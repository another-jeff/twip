from twip.behavior.verb_message_behavior import VerbMessageBehavior


class Pushable(VerbMessageBehavior):
    kind = "pushable"
    verb = "push"


def register() -> None:
    Pushable.register_verb()