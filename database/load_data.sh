#!/bin/bash

set -e # Dừng script nếu bất kỳ lệnh nào thất bại

# echo "▶️  Step 1: Uploading data to datalake..."
# python collect-data/upload-data.py

# echo "✅  Step 1 complete."

# echo "▶️  Step 2: Loading data to PostgreSQL..."
# docker exec database-spark-master-1 spark-submit \
#   --jars jars/delta-core_2.12-2.4.0.jar,\
# jars/delta-storage-2.4.0.jar,\
# jars/hadoop-aws-3.3.4.jar,\
# jars/aws-java-sdk-bundle-1.12.533.jar,\
# jars/postgresql-42.7.3.jar \
#   restaurant_data_processing/main.py

# python restaurant_data_processing/load_data.py

# echo "✅  Step 2 complete, go to http://localhost:8088/ to view the data."

echo "Loading data to PostgreSQL..."
python restaurant_data_processing/load_data.py

echo "✅  Data loaded successfully, go to http://localhost:8088/ to view the data."