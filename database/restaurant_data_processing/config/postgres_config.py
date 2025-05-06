def get_postgres_config():
    return {
        "url": "jdbc:postgresql://db:5432/restaurants",
        "properties": {
            "user": "postgres",
            "password": "example",
            "driver": "org.postgresql.Driver",
            "stringtype": "unspecified"
        }
    }