from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    ok: bool
    message: str
    consumes_turn: bool = False

    @classmethod
    def success(
        cls,
        message: str,
        *,
        consumes_turn: bool = False,
    ) -> "Result":
        return cls(
            ok=True,
            message=message,
            consumes_turn=consumes_turn,
        )

    @classmethod
    def failure(cls, message: str) -> "Result":
        return cls(
            ok=False,
            message=message,
            consumes_turn=False,
        )