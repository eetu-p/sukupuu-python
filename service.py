import database
import datetime

def convert(date: str) -> datetime.date:
    format = "%d.%m.%Y"
    date_obj = datetime.date.strptime(date, format)
    return date_obj

def process_personal_details(
        given_name: str | None, 
        last_name: str | None,
        date_of_birth: str | None, 
        date_of_death: str | None,
    ) -> dict[str, str | datetime.date | None]:

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

    return {
        "given_name": given_name, 
        "last_name": last_name, 
        "date_of_birth": date_of_birth_obj, 
        "date_of_death": date_of_death_obj
    }

##### person-funktiot #########################################################

def add_person(
        given_name: str | None, 
        last_name: str | None,
        date_of_birth: str | None, 
        date_of_death: str | None,
        image: str | None
    ) -> int:

    person_details = process_personal_details(
        given_name,
        last_name,
        date_of_birth,
        date_of_death
    )

    return database.create_person(
        person_details["given_name"], 
        person_details["last_name"], 
        person_details["date_of_birth"], 
        person_details["date_of_death"],
        image
    )

def fetch_person(id: str):
    return database.get_person(id)

def fetch_all_persons():
    return database.get_all_persons()

def modify_person(
        id: str,
        given_name: str | None, 
        last_name: str | None,
        date_of_birth: str | None, 
        date_of_death: str | None,
        image: str | None
    ):

    person_details = process_personal_details(
        given_name,
        last_name,
        date_of_birth,
        date_of_death
    )

    return database.update_person(
        id,
        person_details["given_name"],
        person_details["last_name"],
        person_details["date_of_birth"],
        person_details["date_of_death"],
        image
    )

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