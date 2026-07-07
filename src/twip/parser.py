from twip import direction
from twip.action import Action


ALIASES = {
    "l": "look",
    "x": "examine",
    "i": "inventory",
    "z": "wait",
    "g": "again",
}

PREPOSITIONS = {
    "at",
    "in",
    "into",
    "on",
    "onto",
    "under",
    "behind",
    "with",
    "to",
    "from",
    "about",
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

        if normalized in direction.ALIASES:
            return Action(
                verb="go",
                target=direction.normalize(normalized),
                text=text,
            )

        words = normalized.split(" ", 1)
        verb = ALIASES.get(words[0], words[0])

        if len(words) == 1:
            return Action(verb=verb, target="", text=text)

        target = self._clean_target(words[1])
        target, preposition, target_indirect = self._split_preposition(target)

        return Action(
            verb=verb,
            target=target,
            text=text,
            preposition=preposition,
            target_indirect=target_indirect,
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