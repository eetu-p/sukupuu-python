from connection import get_connection
import datetime

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
            parent_of       SMALLINT references family(id),
            child_of        SMALLINT references family(id)
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()

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

def create_person(
        # TODO: given/last_name sekä parent/child_of voivat olla ainoastaan
        # str | None, date_of_birth/death voivat olla ainoastaan
        # datetime.date | None, poista turhat tyyppivinkit.
        given_name: str | datetime.date | None,
        last_name: str | datetime.date | None,
        date_of_birth: str | datetime.date | None,
        date_of_death: str | datetime.date | None,
        parent_of: str | datetime.date | None,
        child_of: str | datetime.date | None
        ) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    INSERT INTO person (
                        given_name, 
                        last_name, 
                        date_of_birth, 
                        date_of_death,
                        parent_of,
                        child_of
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id;
                ''',
                (
                    given_name, 
                    last_name, 
                    date_of_birth, 
                    date_of_death,
                    parent_of,
                    child_of
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
        # TODO: given/last_name sekä parent/child_of voivat olla ainoastaan
        # str | None, date_of_birth/death voivat olla ainoastaan
        # datetime.date | None, poista turhat tyyppivinkit.
        given_name: str | datetime.date | None,
        last_name: str | datetime.date | None,
        date_of_birth: str | datetime.date | None,
        date_of_death: str | datetime.date | None,
        parent_of: str | datetime.date | None,
        child_of: str | datetime.date | None
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
                        parent_of = %s,
                        child_of = %s
                    WHERE id = %s;
                ''',
                (
                    given_name, 
                    last_name, 
                    date_of_birth, 
                    date_of_death,
                    parent_of,
                    child_of,
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