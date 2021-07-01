from dataclasses import dataclass
from typing import List
from numbers import Number

# Defines a class for easy work with request data


@dataclass(frozen=True)
class MovesInCommon:
    lan: str
    pokemons: List[str]
    limit: Number
