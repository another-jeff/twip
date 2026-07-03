from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    ok: bool
    message: str

    @classmethod
    def success(cls, message: str) -> "Result":
        return cls(ok=True, message=message)

    @classmethod
    def failure(cls, message: str) -> "Result":
        return cls(ok=False, message=message)