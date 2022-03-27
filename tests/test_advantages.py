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


def test_example(client):
    res = client.post(
        "/api/v1/moves", data={"first_type": "water", "second_type": "fire"}
    )
