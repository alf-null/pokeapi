import pytest


@pytest.fixture
def get_first_type():
    return [
        "normal",
        "fighting",
        "flying",
        "poison",
        "ground",
        "rock",
        "bug",
        "ghost",
        "steel",
    ]


@pytest.fixture
def get_second_type():
    return [
        "fairy",
        "dark",
        "dragon",
        "ice",
        "psychic",
        "electric",
        "grass",
        "water",
        "fire",
    ]


def test_advantages(test_app, get_first_type, get_second_type):
    for first_type, second_type in zip(get_first_type, get_second_type):
        a = test_app.post(
            '/api/v1/advantages',
            data={"first_type": first_type, "second_type": second_type},
        )

        print(a)
