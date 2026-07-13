# src/twip/parser.py

from __future__ import annotations

from twip import direction
from twip.action import Action


ALIASES = {
    "l": "look",
    "x": "examine",
    "i": "inventory",
    "z": "wait",
    "g": "again",
}

PREPOSITION_ALIASES = {
    "inside": "in",
    "into": "in",
}

PREPOSITIONS = {
    "at",
    "in",
    "inside",
    "into",
    "on",
    "onto",
    "under",
    "behind",
    "with",
    "to",
    "from",
    "about",
    "through",
}

PREFIX_PREPOSITIONS = {
    "in",
    "inside",
    "into",
    "off",
    "on",
    "to",
    "through",
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
            return Action(verb="", text=text)

        if normalized in direction.ALIASES:
            return Action(
                verb="go",
                text=text,
                target=direction.normalize(normalized),
            )

        words = normalized.split(" ", 1)
        verb = ALIASES.get(words[0], words[0])

        if len(words) == 1:
            return Action(verb=verb, text=text)

        target = self._clean_target(words[1])
        target, preposition, target_indirect = self._split_preposition(target)

        return Action(
            verb=verb,
            text=text,
            target=target,
            preposition=preposition,
            target_indirect=target_indirect,
        )

    def _split_preposition(
        self,
        target: str,
    ) -> tuple[str | None, str | None, str | None]:
        words = target.split()

        if len(words) == 1 and words[0] == "up":
            return None, "up", None

        if words and words[0] in PREFIX_PREPOSITIONS:
            return (
                self._clean_optional_target(
                    " ".join(words[1:])
                ),
                self._normalize_preposition(words[0]),
                None,
            )

        if words and words[-1] in POSTFIX_PREPOSITIONS:
            return (
                self._clean_optional_target(
                    " ".join(words[:-1])
                ),
                self._normalize_preposition(words[-1]),
                None,
            )

        for index, word in enumerate(words):
            if word not in PREPOSITIONS:
                continue

            direct = " ".join(words[:index])
            indirect = " ".join(words[index + 1 :])

            if direct and indirect:
                return (
                    self._clean_target(direct),
                    self._normalize_preposition(word),
                    self._clean_target(indirect),
                )

        return target, None, None

    def _normalize_preposition(
        self,
        preposition: str,
    ) -> str:
        return PREPOSITION_ALIASES.get(
            preposition,
            preposition,
        )

    def _clean_optional_target(self, target: str) -> str | None:
        cleaned = self._clean_target(target)

        if not cleaned:
            return None

        return cleaned

    def _clean_target(self, target: str) -> str:
        for article in ("the ", "a ", "an "):
            if target.startswith(article):
                return target[len(article) :]

        return target