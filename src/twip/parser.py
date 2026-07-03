from twip.action import Action


class Parser:
    def parse(self, text: str) -> Action:
        normalized = " ".join(text.strip().lower().split())

        if not normalized:
            return Action(verb="", target="", text=text)

        words = normalized.split(" ", 1)

        if len(words) == 1:
            return Action(verb=words[0], target="", text=text)

        verb, target = words
        target = self._clean_target(target)

        return Action(verb=verb, target=target, text=text)

    def _clean_target(self, target: str) -> str:
        for article in ("the ", "a ", "an "):
            if target.startswith(article):
                return target[len(article) :]

        return target