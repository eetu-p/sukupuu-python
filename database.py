from connection import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id              SMALLSERIAL PRIMARY KEY,
            given_name      VARCHAR(128),
            last_name       VARCHAR(128),
            date_of_birth   DATE,
            date_of_death   DATE
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()

def create_person(
        given_name,
        last_name,
        date_of_birth,
        date_of_death
        ):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    INSERT INTO person (
                        given_name, 
                        last_name, 
                        date_of_birth, 
                        date_of_death
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                ''',
                (given_name, last_name, date_of_birth, date_of_death)
            )

            return cur.fetchone()[0]