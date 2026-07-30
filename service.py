import database
import datetime

def convert(date: str) -> datetime.date:
    format = "%d.%m.%Y"
    date_obj = datetime.date.strptime(date, format)
    return date_obj

def add_person(
        given_name: str | None, 
        last_name: str | None,
        date_of_birth: str | None, 
        date_of_death: str | None
    ) -> int:

    date_of_birth_obj = None
    date_of_death_obj = None

    if given_name is not None and len(given_name) > 128:
        raise ValueError("Given name cannot be longer than 128 characters.")
    if last_name is not None and len(last_name) > 128:
        raise ValueError("Last name cannot be longer than 128 characters.")
    if date_of_birth is not None:
        date_of_birth_obj = convert(date_of_birth)
        if date_of_birth_obj > datetime.date.today():
            raise ValueError("Date of birth cannot be in the future.")
    if date_of_death is not None:
        date_of_death_obj = convert(date_of_death)
        if date_of_death_obj > datetime.date.today():
            raise ValueError("Date of death cannot be in the future.")
    if (
        date_of_birth_obj is not None
        and date_of_death_obj is not None
        and date_of_death_obj < date_of_birth_obj
    ):
        raise ValueError("Date of death cannot be after date of birth.")

    return database.create_person(
        given_name, 
        last_name, 
        date_of_birth_obj, 
        date_of_death_obj
    )

def fetch_person(id: str):
    return database.get_person(id)