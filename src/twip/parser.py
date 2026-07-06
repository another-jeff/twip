from twip.action import Action


ALIASES = {
    "l": "look",
    "x": "examine",
    "i": "inventory",
    "z": "wait",
    "g": "again",
}

DIRECTIONS = {
    "n": "north",
    "north": "north",
    "e": "east",
    "east": "east",
    "s": "south",
    "south": "south",
    "w": "west",
    "west": "west",
    "ne": "northeast",
    "northeast": "northeast",
    "se": "southeast",
    "southeast": "southeast",
    "nw": "northwest",
    "northwest": "northwest",
    "sw": "southwest",
    "southwest": "southwest",
    "u": "up",
    "up": "up",
    "d": "down",
    "down": "down",
    "in": "in",
    "out": "out",
}

PREPOSITIONS = {
    "about",
    "in",
    "off",
    "on",
    "to",
    "under",
    "with",
}

PREFIX_PREPOSITIONS = {
    "in",
    "off",
    "on",
    "to",
    "under",
}

POSTFIX_PREPOSITIONS = {
    "off",
    "on",
}

class Parser:
    def parse(self, text: str) -> Action:
        normalized = " ".join(text.strip().lower().split())

        if not normalized:
            return Action(verb="", target="", text=text)

        if normalized in DIRECTIONS:
            return Action(
                verb="go",
                target=DIRECTIONS[normalized],
                text=text,
            )

        words = normalized.split(" ", 1)
        verb = ALIASES.get(words[0], words[0])

        if len(words) == 1:
            return Action(verb=verb, target="", text=text)

        target = self._clean_target(words[1])
        target, preposition, indirect_target = self._split_preposition(target)

        return Action(
            verb=verb,
            target=target,
            text=text,
            preposition=preposition,
            indirect_target=indirect_target,
        )

    def _split_preposition(self, target: str) -> tuple[str, str, str]:
        words = target.split()

        if len(words) == 1 and words[0] == "up":
            return "", "up", ""

        if words and words[0] in PREFIX_PREPOSITIONS:
            return (
                self._clean_target(" ".join(words[1:])),
                words[0],
                "",
            )

        if words and words[-1] in POSTFIX_PREPOSITIONS:
            return (
                self._clean_target(" ".join(words[:-1])),
                words[-1],
                "",
            )

        for index, word in enumerate(words):
            if word not in PREPOSITIONS:
                continue

            direct = " ".join(words[:index])
            indirect = " ".join(words[index + 1 :])

            if direct and indirect:
                return (
                    self._clean_target(direct),
                    word,
                    self._clean_target(indirect),
                )

        return target, "", ""

    def _clean_target(self, target: str) -> str:
        for article in ("the ", "a ", "an "):
            if target.startswith(article):
                return target[len(article) :]

        return target