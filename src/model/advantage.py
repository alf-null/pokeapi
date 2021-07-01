from dataclasses import dataclass

# Defines a class for easy work with request data
@dataclass(frozen=True)
class AdvantageTypes:
    first_type: str
    second_type: str
