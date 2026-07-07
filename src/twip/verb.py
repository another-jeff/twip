from dataclasses import dataclass


@dataclass(frozen=True)
class Verb:
    name: str
    requires_target: bool = True

def register_verb(
    name: str,
    *,
    requires_target: bool = True,
    replace: bool = False,
) -> None:
    if not replace and name in VERBS:
        raise ValueError(f"Verb is already registered: {name}")

    VERBS[name] = Verb(name, requires_target=requires_target)

VERBS = {
    "about": Verb("about", requires_target=False),
    "again": Verb("again", requires_target=False),
    "curse": Verb("curse", requires_target=False),
    "help": Verb("help", requires_target=False),
    "info": Verb("info", requires_target=False),
    "inventory": Verb("inventory", requires_target=False),
    "jump": Verb("jump", requires_target=False),
    "listen": Verb("listen", requires_target=False),
    "look": Verb("look", requires_target=False),
    "pray": Verb("pray", requires_target=False),
    "sing": Verb("sing", requires_target=False),
    "sleep": Verb("sleep", requires_target=False),
    "undo": Verb("undo", requires_target=False),
    "wait": Verb("wait", requires_target=False),
    "wake": Verb("wake", requires_target=False),

    "ask": Verb("ask"),
    "break": Verb("break"),
    "burn": Verb("burn"),
    "climb": Verb("climb"),
    "dig": Verb("dig"),
    "drink": Verb("drink"),
    "drop": Verb("drop"),
    "eat": Verb("eat"),
    "enter": Verb("enter"),
    "examine": Verb("examine"),
    "feel": Verb("feel"),
    "fill": Verb("fill"),
    "give": Verb("give"),
    "go": Verb("go"),
    "open": Verb("open"),
    "pull": Verb("pull"),
    "push": Verb("push"),
    "put": Verb("put"),
    "search": Verb("search"),
    "show": Verb("show"),
    "smell": Verb("smell"),
    "take": Verb("take"),
    "talk": Verb("talk"),
    "tell": Verb("tell"),
    "turn": Verb("turn"),
    "unlock": Verb("unlock"),
    "wave": Verb("wave"),
    "wear": Verb("wear"),
}