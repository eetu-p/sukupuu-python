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

def get_connection():
    return psycopg2.connect(
        host = HOSTNAME,
        dbname = DATABASE_NAME,
        user = USERNAME,
        password = PASSWORD,
        port = PORT
    )