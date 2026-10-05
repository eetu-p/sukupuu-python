from dataclasses import dataclass
from datetime import date

@dataclass
class Person:
    id: int | None
    given_name: str | None
    last_name: str | None
    date_of_birth: date | None
    date_of_death: date | None
    image: str | None

@dataclass
class Family:
    id: int | None

@dataclass
class Relationship:
    person_id: int
    family_id: int
    role: str

@dataclass
class GraphCustomization:
    date_format: str = "%d.%m.%Y"
    family_fill_color: str | None = "white"
    family_font_color: str | None = None
    family_height: str | None = None
    family_shape: str | None = "ellipse"
    family_show_id: bool | None = True
    family_width: str | None = None
    fill_color: str | None = "white"
    font_color: str | None = None
    font_name: str | None = None
    font_size: str | None = None
    height: str | None = None
    name_font_bold: bool | None = True
    name_font_size: str | None = "14"
    shape: str | None = "rectangle"
    show_id: bool | None = True
    width: str | None = None