# Grab-Bootcamp-Backend-2025

I recommend using [uv](https://github.com/astral-sh/uv) for package management but you can use `pip` or `conda` if you prefer.

## Install

```bash
uv venv --python 3.12.0
.venv\Scripts\activate
uv pip install -r requirements.txt
```

## Dev

```bash
fastapi dev src/main.py
```

## Test

Go to `http://127.0.0.1:8000/docs` to see the API docs.