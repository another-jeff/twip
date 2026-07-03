from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    succeeded: bool
    message: str

    @classmethod
    def success(cls, message: str) -> "Result":
        return cls(succeeded=True, message=message)

    @classmethod
    def failure(cls, message: str) -> "Result":
        return cls(succeeded=False, message=message)