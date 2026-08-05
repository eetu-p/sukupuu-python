import database
import datetime
from models import Person

def validate_personal_details(
        given_name: str | None, 
        last_name: str | None,
        date_of_birth: datetime.date | None, 
        date_of_death: datetime.date | None,
    ):
    
    if given_name is not None and len(given_name) > 128:
        raise ValueError("Given name cannot be longer than 128 characters.")
    if last_name is not None and len(last_name) > 128:
        raise ValueError("Last name cannot be longer than 128 characters.")
    if date_of_birth is not None:
        if date_of_birth > datetime.date.today():
            raise ValueError("Date of birth cannot be in the future.")
    if date_of_death is not None:
        if date_of_death > datetime.date.today():
            raise ValueError("Date of death cannot be in the future.")
    if (
        date_of_birth is not None
        and date_of_death is not None
        and date_of_death < date_of_birth
    ):
        raise ValueError("Date of death cannot be after date of birth.")

##### person-funktiot #########################################################

def add_person(person: Person) -> int:
    validate_personal_details(
        person.given_name,
        person.last_name,
        person.date_of_birth,
        person.date_of_death
    )

    return database.create_person(person)

def fetch_person(id: str):
    return database.get_person(id)

def fetch_all_persons():
    return database.get_all_persons()

def modify_person(person: Person):
    validate_personal_details(
        person.given_name,
        person.last_name,
        person.date_of_birth,
        person.date_of_death
    )

    return database.update_person(person)

def remove_person(id: str):
    return database.delete_person(id)

##### family-funktiot #########################################################

def add_family() -> int:
    return database.create_family()

def fetch_all_families():
    return database.get_all_families()

def remove_family(id: int):
    return database.delete_family(id)

##### person-family-funktiot ##################################################

role_types = ["parent", "child", "adopted_child"]

def add_relationship(person_id: str, family_id: str, role: str):
    if role not in role_types:
        raise ValueError("Invalid role.")

    return database.create_relationship(person_id, family_id, role)

def fetch_all_relationships():
    return database.get_all_relationships()

def remove_relationship(person_id: str, family_id: str):
    return database.delete_relationship(person_id, family_id)