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

## If using qdrant local
In folder vector_db, download this file and add to this folder (this file contains embedding vectors of images) : [Image Embedding](https://drive.google.com/file/d/1TfGRQ-N2x_ZW1r-qQQXJ-0FzUQqjFg1H/view?usp=sharing)
In folder root (Grab-Bootcamp-Backend-2025)
```bash
docker run -d -p 6333:6333 qdrant/qdrant
python -m vector_db.load_embedding
```


## Dev

```bash
fastapi dev src/main.py
```

## Test

Go to `http://127.0.0.1:8000/docs` to see the API docs.