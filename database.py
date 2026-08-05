from connection import get_connection
from models import Person, Family, Relationship
from typing import List

##### person-taulukon funktiot ################################################

def create_person_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS person (
                    id              SMALLSERIAL PRIMARY KEY,
                    given_name      VARCHAR(128),
                    last_name       VARCHAR(128),
                    date_of_birth   DATE,
                    date_of_death   DATE,
                    image           TEXT
                );
            ''')

def create_person(person: Person) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    INSERT INTO person (
                        given_name, 
                        last_name, 
                        date_of_birth, 
                        date_of_death,
                        image
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (
                    person.given_name, 
                    person.last_name, 
                    person.date_of_birth, 
                    person.date_of_death,
                    person.image
                )
            )

            # Pylance antaa "Object of type None is not subscriptable"
            # varoituksen, jos ennen cur.fetchone()-metodin indeksointia
            # ei ole varmistettu, että sen arvo ei ole None.
            # TODO: uudelleennimeä person_row -> row
            person_row = cur.fetchone()
            if person_row is None:
                raise RuntimeError("INSERT did not return an ID.")
            return person_row[0]

def get_person(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT * 
                    FROM person 
                    WHERE id = %s
                ''',
                (id,)
            )

            row = cur.fetchone()

            if row is None:
                return None
            
            return Person(row[0], row[1], row[2], row[3], row[4], row[5])

def get_all_persons() -> list[Person]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT *
                FROM person
            ''')

            rows = cur.fetchall()
            persons: List[Person] = []

            for row in rows:
                persons.append(Person(
                    row[0], row[1], row[2], row[3], row[4], row[5]
                ))

            return persons

            
def update_person(person: Person):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    UPDATE person 
                    SET 
                        given_name = %s,
                        last_name = %s,
                        date_of_birth = %s,
                        date_of_death = %s,
                        image = %s
                    WHERE id = %s;
                ''',
                (
                    person.given_name, 
                    person.last_name, 
                    person.date_of_birth, 
                    person.date_of_death,
                    person.image,
                    person.id
                )
            )

def delete_person(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    DELETE FROM person
                    WHERE id = %s
                ''',
                (id,)
            )

##### family-taulukon funktiot ################################################

def create_family_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS family (
                    id          SMALLSERIAL PRIMARY KEY
                );
            ''')

def create_family() -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO family
                DEFAULT VALUES
                RETURNING id;
            ''')

            # Pylance antaa "Object of type None is not subscriptable"
            # varoituksen, jos ennen cur.fetchone()-metodin indeksointia
            # ei ole varmistettu, että sen arvo ei ole None.
            family_row = cur.fetchone()
            if family_row is None:
                raise RuntimeError("INSERT did not return an ID.")
            return family_row[0]

def get_all_families() -> list[Family]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT *
                FROM family
            ''')

            rows = cur.fetchall()
            families: List[Family] = []

            for row in rows:
                families.append(Family(row[0]))

            return families

def delete_family(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    DELETE FROM family
                    WHERE id = %s
                ''',
                (id,)
            )

##### person_family-taulukon funktiot #########################################

def create_person_family_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS person_family (
                    person_id   SMALLINT REFERENCES person(id),
                    family_id   SMALLINT REFERENCES family(id),
                    role        TEXT 
                                CONSTRAINT role_type 
                                CHECK (role IN (
                                        'parent',
                                        'child',
                                        'adopted_child'
                                    )
                                ),
                    PRIMARY KEY (person_id, family_id)
                );
            ''')

def create_relationship(relationship: Relationship):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    INSERT INTO person_family (
                        person_id,
                        family_id,
                        role
                    )
                    VALUES (%s, %s, %s)
                ''', 
                (
                    relationship.person_id, 
                    relationship.family_id, 
                    relationship.role
                )
            )

def get_all_relationships() -> list[Relationship]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT *
                FROM person_family;
            ''')

            rows = cur.fetchall()
            relationships: List[Relationship] = []

            for row in rows:
                relationships.append(Relationship(row[0], row[1], row[2]))

            return relationships

def delete_relationship(person_id: int, family_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    DELETE FROM person_family
                    WHERE person_id = %s 
                    AND family_id = %s;
                ''', (person_id, family_id)
            )