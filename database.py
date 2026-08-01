from connection import get_connection
import datetime

##### person-taulukon funktiot ################################################

def create_person_table():
    conn = get_connection()
    cur = conn.cursor()

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

    conn.commit()
    cur.close()
    conn.close()

def create_person(
        # TODO: mikään parametreista ei voi olla joko str tai datetime.date,
        # poista turhat tyyppivinkit.
        given_name: str | datetime.date | None,
        last_name: str | datetime.date | None,
        date_of_birth: str | datetime.date | None,
        date_of_death: str | datetime.date | None,
        image: str | datetime.date | None
        ) -> int:
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
                    given_name, 
                    last_name, 
                    date_of_birth, 
                    date_of_death,
                    image
                )
            )

            # Pylance antaa "Object of type None is not subscriptable"
            # varoituksen, jos ennen cur.fetchone()-metodin indeksointia
            # ei ole varmistettu, että sen arvo ei ole None.
            person_row = cur.fetchone()
            if person_row is None:
                raise RuntimeError("INSERT did not return an ID.")
            return person_row[0]

def get_person(id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT * 
                    FROM person 
                    WHERE id = %s
                ''',
                (id,)
            )

            return cur.fetchone()

def get_all_persons():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT *
                FROM person
            ''')

            return cur.fetchall()

def update_person(
        # TODO: mikään parametreista ei voi olla joko str tai datetime.date,
        # poista turhat tyyppivinkit.
        id: str,
        given_name: str | datetime.date | None,
        last_name: str | datetime.date | None,
        date_of_birth: str | datetime.date | None,
        date_of_death: str | datetime.date | None,
        image: str | datetime.date | None
    ):
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
                    given_name, 
                    last_name, 
                    date_of_birth, 
                    date_of_death,
                    image,
                    id
                )
            )

def delete_person(id: str):
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
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS family (
            id          SMALLSERIAL PRIMARY KEY
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()

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

def get_all_families():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT *
                FROM family
            ''')

            return cur.fetchall()

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

def create_relationship(person_id: str, family_id: str, role: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    INSERT INTO person_family (
                        person_id,
                        family_id,
                        role
                    )
                    VALUES (%s, %s, %s)
                ''', (person_id, family_id, role)
            )

def get_all_relationships():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT *
                FROM person_family;
            ''')

            return cur.fetchall()

def delete_relationship(person_id: str, family_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    DELETE FROM person_family
                    WHERE person_id = %s 
                    AND family_id = %s;
                ''', (person_id, family_id)
            )