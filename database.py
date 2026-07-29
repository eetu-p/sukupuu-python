import psycopg2
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

HOSTNAME = os.getenv("HOSTNAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = HOSTNAME,
        dbname = DATABASE_NAME,
        user = USERNAME,
        password = PASSWORD,
        port = PORT
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