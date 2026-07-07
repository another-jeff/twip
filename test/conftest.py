# test/conftest.py

import pytest

from twip.verb import VERBS


@pytest.fixture
def restore_verbs():
    original = VERBS.copy()
    try:
        yield
    finally:
        VERBS.clear()
        VERBS.update(original)