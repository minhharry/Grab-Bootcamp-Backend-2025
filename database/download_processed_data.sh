#!/bin/bash

set -e # Dừng script nếu bất kỳ lệnh nào thất bại

echo "▶️  Step 1: Uploading data to datalake..."
python collect_data/upload_data_to_minIO.py

echo "✅  Step 1 complete."

echo "▶️  Step 2: Loading processed to processed_data folder and data of the images table to the images_table_data folder"
docker exec database-spark-master-1 spark-submit \
  --jars jars/delta-core_2.12-2.4.0.jar,\
jars/delta-storage-2.4.0.jar,\
jars/hadoop-aws-3.3.4.jar,\
jars/aws-java-sdk-bundle-1.12.533.jar,\
jars/postgresql-42.7.3.jar \
  restaurant_data_processing/normalize_data.py

echo "✅  Step 2 complete, go to the processed_data and images_table_data folders to view the data."
