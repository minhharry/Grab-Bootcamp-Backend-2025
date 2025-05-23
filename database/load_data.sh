#!/bin/bash

# dos2unix load_data.sh  # convert line endings from Windows to Unix

set -e # Dừng script nếu bất kỳ lệnh nào thất bại

echo "Loading data to PostgreSQL..."
../.venv/Scripts/python.exe restaurant_data_processing/load_data_from_jsonl_to_postgres.py

echo "✅  Data loaded successfully, go to http://localhost:8088/ to view the data."