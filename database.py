import psycopg2

hostname = 'localhost'
database_name = 'Sukupuuohjelma'
username = 'eetu'
password = '1234'
port = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database_name,
        user = username,
        password = password,
        port = port
    )

    cur = conn.cursor()

    create_script = '''
        CREATE TABLE IF NOT EXISTS person (
            id      int PRIMARY KEY,
            given_name    varchar(128) NOT NULL,
            last_name     varchar(128) NOT NULL,
            date_of_birth   date,
            date_of_death   date
        )
    '''
    cur.execute(create_script)

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()