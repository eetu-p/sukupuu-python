from dataclasses import dataclass
from datetime import date

@dataclass
class Person:
    id: int
    given_name: str | None
    last_name: str | None
    date_of_birth: date | None
    date_of_death: date | None
    image: str | None

@dataclass
class Family:
    id: int

@dataclass
class Relationship:
    person_id: int
    family_id: int
    role: str