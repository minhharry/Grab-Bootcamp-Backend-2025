# Grab-Bootcamp-Backend-2025

I recommend using [uv](https://github.com/astral-sh/uv) for package management but you can use `pip` or `conda` if you prefer.


## Install

```bash
uv venv --python 3.12.0
.venv\Scripts\activate
uv pip install -r requirements.txt
```
## In database/ add file .env
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
POSTGRES_DB=restaurants
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=12345678
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

`Running these commands for the first time may take a while.`

Navigate to the `database` directory:
```sh
cd database
```

Download Spark libraries: (skip if previously done)
```sh
bash download_jars.sh
pip install minio==7.2.15 
```

Run Docker Compose to initialize the containers:
```sh
docker compose up -d
```

Load data to Postgres:
```sh
bash load_data.sh
```

Go to `http://localhost:8088/` to view all the data. (`Note: Adminer port has been change from 8080 to 8088.`)

Delete everything with the `-v` flag:
```sh
docker compose down -v
```

## In src/routers/image_search add file .env
```bash
QDRANT_URL=
API_KEY=
```

## If using qdrant local
In folder vector_db, download image_vectors.csv in this folder [Image Embedding](https://drive.google.com/drive/folders/1nKzVk1eyjutBAYo34F7gatrBIcarMyNY?usp=sharing) and add to vector_db folder  

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

```bash
cd src
pytest test.py
```

Go to `http://127.0.0.1:8000/docs` to see the API docs.
