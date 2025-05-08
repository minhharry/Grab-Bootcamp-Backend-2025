import os

def get_postgres_config():
    return {
        "url": "jdbc:postgresql://db:5432/restaurants",
        "properties": {
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "driver": "org.postgresql.Driver",
            "stringtype": "unspecified"
        }
    }