# Grab-Bootcamp-Backend-2025

I recommend using [uv](https://github.com/astral-sh/uv) for package management but you can use `pip` or `conda` if you prefer.


## Install

```bash
uv venv --python 3.12.0
.venv\Scripts\activate
uv pip install -r requirements.txt
```
## In src/ add file .env
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
POSTGRES_DB=restaurants
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```
## Run the database

Just run docker compose to initalize the database:
```sh
docker compose -f database/docker-compose.yaml up
```
Note: Add the --build flag to force a rebuild of the image if you make changes to the code in load-data.py to ensure the updated code is built into the new image. (`docker compose -f database/docker-compose.yaml up --build`)

If any errors occur, try deleting everything and running again with:
```sh
docker compose -f database/docker-compose.yaml down -v
```
Note: The -v flag deletes everything (including data). Afterward, run `docker compose -f database/docker-compose.yaml up` to load the data into the database again.

Go to `http://localhost:8080/` to view all the data.

## In src/routers/image_search add file .env
```bash
QDRANT_URL=
API_KEY=
```
## Dev

```bash
fastapi dev src/main.py
```

## Test

Go to `http://127.0.0.1:8000/docs` to see the API docs.
