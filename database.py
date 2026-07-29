import psycopg2

hostname = 'localhost'
database_name = 'Sukupuuohjelma'
username = 'postgres'
password = '1234'
port = 5432

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database_name,
        user = username,
        password = password,
        port = port
    )

    conn.close()
except Exception as error:
    print(error)