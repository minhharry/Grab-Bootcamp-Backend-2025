# Grab-Bootcamp-Backend-2025

I recommend using [uv](https://github.com/astral-sh/uv) for package management but you can use `pip` or `conda` if you prefer.


## Install

```bash
uv venv --python 3.12.0
.venv\Scripts\activate
uv pip install -r requirements.txt
```
## Config database
```bash
cd database
```
and follow this README file https://github.com/minhharry/Grab-Bootcamp-Backend-2025/blob/phuc/database/readme.md
```bash
cd ..
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