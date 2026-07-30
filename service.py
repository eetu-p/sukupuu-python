import database
import datetime

def convert(date):
    format = "%d.%m.%Y"
    date_obj = datetime.date.strptime(date, format)
    return date_obj

def add_person(given_name, last_name, date_of_birth, date_of_death):
    if given_name is not None and len(given_name) > 128:
        raise ValueError("Given name cannot be longer than 128 characters.")
    if last_name is not None and len(last_name) > 128:
        raise ValueError("Last name cannot be longer than 128 characters.")
    if date_of_birth is not None:
        date_of_birth = convert(date_of_birth)
        if date_of_birth > datetime.date.today():
            raise ValueError("Date of birth cannot be in the future.")
    if date_of_death is not None:
        date_of_death = convert(date_of_death)
        if date_of_death > datetime.date.today():
            raise ValueError("Date of death cannot be in the future.")
    if (
        date_of_birth is not None
        and date_of_death is not None
        and date_of_death < date_of_birth
    ):
        raise ValueError("Date of death cannot be after date of birth.")

    return database.create_person(
        given_name, 
        last_name, 
        date_of_birth, 
        date_of_death
    )

def fetch_person(id):
    return database.get_person(id)