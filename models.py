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

# Oma Date-luokka luodaan siksi, että Pythonin datetime.date-luokassa päivä ja
# kuukausi ovat pakollisia. Syntymä- ja kuolinpäivistä ei usein kuitenkaan
# tiedetä päivää tai kuukautta, tämä luokka soveltuu sellaisiin tapauksiin.
# Lisäksi myöhemmin ehkä lisätään ominaisuus, jossa syntymä/kuolinajan voi
# ilmaista vaikkapa aikavälinä (esim. 1932-1934), jolloin itse tehdystä
# Date-luokasta voi olla hyötyä.
@dataclass
class Date:
    day: int | None
    month: int | None
    year: int

    def get_string(self, separator: str = ".") -> str:
        return (
            f"{'' if self.day is None else (str(self.day) + separator)}" 
            f"{'' if self.month is None else (str(self.month) + separator)}"
            f"{self.year}"
        )
        

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