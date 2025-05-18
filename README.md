# Grab-Bootcamp-Backend-2025

<img src="https://private-user-images.githubusercontent.com/122473375/444859039-e20210db-0545-4f62-a070-a7d90d5445fa.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDc1NDg0NTAsIm5iZiI6MTc0NzU0ODE1MCwicGF0aCI6Ii8xMjI0NzMzNzUvNDQ0ODU5MDM5LWUyMDIxMGRiLTA1NDUtNGY2Mi1hMDcwLWE3ZDkwZDU0NDVmYS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNTE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDUxOFQwNjAyMzBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wNzdhYjM4NTg1ZGE2YTcwOWRhMWU2NWZkNDZkNzg1NjhiODUxN2MxZDYzNDEyYTVmNzNhMGZhNTQ3MzU0M2IwJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.xdzroWwowqec8711s4xjOx-N341FDdFOL79IdFPhHH0" width="700">

## ⬇️ **Video demo below here** ⬇️
[<img src="https://img.youtube.com/vi/kNpFvkHNI3M/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=kNpFvkHNI3M)

I recommend using [uv](https://github.com/astral-sh/uv) for package management but you can use `pip` or `conda` if you prefer.


## Install

```bash
uv venv --python 3.12.0
.venv\Scripts\activate
uv pip install -r requirements.txt
```
## In database/ add file .env
```bash
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
MINIO_ROOT_USER=
MINIO_ROOT_PASSWORD=
```
## In src/ add file .env
```bash
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```
## Run the database

Running these commands for the first time may take a while.

### Load The Provided Restaurant data:
1. **Navigate to the `database` directory**:
```sh
cd database
```

2. **Run Docker Compose to initialize the containers**:
```sh
docker compose up -d
```

3. **Load the provided processed data to Postgres**:
```sh
bash load_data.sh
```

Go to `http://localhost:8088/` to view all the data. (`Note: Adminer port has been change from 8080 to 8088.`)

### (Optional) Collecting and Processing More Restaurant Data:
1. **Download Spark libraries: (skip if previously done)**
```sh
bash download_jars.sh
pip install minio==7.2.15 
```
2. **Collect restaurant data**:
- From GoogleMaps:
```sh
python database/collect_data/collect_data_ggmap/main.py
```
- From Shopeefood:
```sh
python database/collect_data/collect_data_shopeefood/main.py
```

3. **Process the raw data**:
   - Select the collection date to process: set the target date in `global_config.py`.
   - Run the normalization script:
     ```bash
     bash normalize_data.sh
     ```
   - Use the food recognition model to fill missing values in the `food_name` column:  
     [Open the Kaggle Notebook](https://www.kaggle.com/code/colabnguyen/recognize-food-name-and-embedding) 

   - Get restaurant coordinates (longitude, latitude):
     - Add `GOMAPS_API_KEY` to `database/.env`.  
       You can get a free API key at [GoMaps](https://app.gomaps.pro/)
     - Get locations:
       ```bash
       python get_locations.py
       ```

### (Optional) Add dummy User and User clicks data:
```sh
cd dummy_users_data
python createDummyUserAndUserClicksData.py
```

## In src/routers/image_search add file .env
```bash
QDRANT_URL=
API_KEY=
```

## If using qdrant local
In folder vector_db, download image_vectors.csv in this folder [Image Embedding](https://drive.google.com/drive/folders/1nKzVk1eyjutBAYo34F7gatrBIcarMyNY?usp=drive_link) and add to vector_db folder  

In folder root (Grab-Bootcamp-Backend-2025)
```bash
docker run -d -p 6333:6333 qdrant/qdrant
python -m vector_db.load_embedding
```

Or you can generate image embeddings yourself using our Kaggle notebook:
 👉 [Open the Kaggle Notebook](https://www.kaggle.com/code/colabnguyen/recognize-food-name-and-embedding) 
Steps:
1. Click "Copy and Edit" to create your own version of the notebook.

2. In the notebook editor, click "Save Version" → "Advanced Settings".

3. Under the "Accelerator" dropdown, select GPU for all sections.

4. Click "Save & Run All (Commit)".

- Kaggle will execute the entire notebook automatically in the background — you can safely close your browser or shut down your device.

5. Once the run completes, go to the "Versions" tab of your notebook.

6. Open the latest version and navigate to the "Output" section.

7. Download the generated image_vectors.csv file.
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
