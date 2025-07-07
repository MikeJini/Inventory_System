# config.py
import os
import psycopg2
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

dbname = "inventory"
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

print(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")

time.sleep(10)
print("Program resumed after 10 seconds.")

class Config:

    SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def create_database():
        
        # Connect to default "postgres" database
        connection = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create cursor and database
        cursor = connection.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {dbname}")
        except psycopg2.errors.DuplicateDatabase:
            print("Database already made, skipping...")

        cursor.close()
        connection.close()
        print(f"Database '{dbname}' is up.")
