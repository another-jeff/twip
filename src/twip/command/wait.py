from twip.result import Result

def handle(world, action) -> Result:
    return Result.success(
        "Time passes.",
        consumes_turn=True,
    )