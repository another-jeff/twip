from twip.entity import Entity
from twip.language import English


def entity(name: str) -> Entity:
    return Entity(names=(name,))


def test_indefinite_uses_a_before_consonant():
    language = English()

    assert language.indefinite_text("coin") == "a coin"


def test_indefinite_uses_an_before_vowel():
    language = English()

    assert language.indefinite_text("apple") == "an apple"


def test_definite_uses_the():
    language = English()

    assert language.definite_text("coin") == "the coin"


def test_entity_list_with_no_entities():
    language = English()

    assert language.entity_list(
        [],
        language.indefinite,
    ) == "nothing"


def test_entity_list_with_one_entity():
    language = English()

    assert language.entity_list(
        [entity("coin")],
        language.indefinite,
    ) == "a coin"


def test_entity_list_with_two_entities():
    language = English()

    assert language.entity_list(
        [
            entity("key"),
            entity("coin"),
        ],
        language.indefinite,
    ) == "a coin and a key"


def test_entity_list_with_three_entities():
    language = English()

    assert language.entity_list(
        [
            entity("key"),
            entity("coin"),
            entity("apple"),
        ],
        language.indefinite,
    ) == "an apple, a coin, and a key"


def test_entity_list_can_use_definite_phrases():
    language = English()

    assert language.entity_list(
        [
            entity("key"),
            entity("coin"),
        ],
        language.definite,
    ) == "the coin and the key"