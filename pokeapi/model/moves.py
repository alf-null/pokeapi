from dataclasses import dataclass
from numbers import Number
from typing import List

# Defines a class for easy work with request data


@dataclass(frozen=True)
class MovesInCommon:
    lan: str
    pokemons: List[str]
    limit: Number
