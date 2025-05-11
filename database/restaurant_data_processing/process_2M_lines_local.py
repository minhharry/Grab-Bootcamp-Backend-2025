import time
import json
import tempfile
import os
import logging
from pyspark.sql import SparkSession
from schemas.shopeefood_raw_schema import shopeefood_raw_schema
from data_processing.shopee_processing import process_shopee_data
from config.postgres_config import get_postgres_config
from load_data.write_from_spark_to_postgres import write_to_postgres
from config.spark_config import init_spark

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_large_jsonl_in_chunks(file_path, chunk_size=250, start_chunk=0):
    with open(file_path, 'rb') as f:
        buffer = []
        chunk_count = 0
        line_count = 0
        
        for line in f:
            line_count += 1
            if chunk_count < start_chunk:
                if line_count % chunk_size == 0:
                    chunk_count += 1
                continue
            
            buffer.append(line)
            if len(buffer) == chunk_size:
                chunk_count += 1
                yield chunk_count, b'\n'.join(buffer)
                buffer = []
        
        if buffer:
            chunk_count += 1
            yield chunk_count, b'\n'.join(buffer)

def process_chunk(spark, file_path, chunk_size=250, checkpoint_file="checkpoints/chunk_progress.json"):
    temp_dir = tempfile.mkdtemp()
    postgres_config = get_postgres_config()
    
    start_chunk = 0
    if os.path.exists(checkpoint_file):
        try:
            with open(checkpoint_file, "r") as f:
                checkpoint_data = json.load(f)
                if checkpoint_data.get(file_path):
                    start_chunk = checkpoint_data[file_path]
            print(f"Resuming from chunk {start_chunk} for {file_path}")
        except Exception as e:
            logger.warning(f"Error reading checkpoint file: {e}, starting from chunk 0")
    
    try:
        for chunk_id, chunk in read_large_jsonl_in_chunks(file_path, chunk_size, start_chunk):
            temp_file = f"{temp_dir}/chunk_{chunk_id}.json"
            with open(temp_file, "wb") as f:
                f.write(chunk)
            
            df = spark.read.schema(shopeefood_raw_schema).json(temp_file)
            record_count = df.count()
            if record_count == 0:
                print(f"Chunk {chunk_id} is empty, skipping")
                os.remove(temp_file)
                continue
            
            # print(f"Processing chunk {chunk_id} with {record_count} records")
            
            processed_df = process_shopee_data(spark, df)
            
            # print(f"Writing chunk {chunk_id} to PostgreSQL")
            write_to_postgres(processed_df, postgres_config)
            print(f"Write chunk {chunk_id} to PostgreSQL done")
            
            checkpoint_data = {file_path: chunk_id}
            os.makedirs(os.path.dirname(checkpoint_file), exist_ok=True)
            with open(checkpoint_file, "w") as f:
                json.dump(checkpoint_data, f)
            # print(f"Updated checkpoint for chunk {chunk_id}")
            
            processed_df.unpersist()
            df.unpersist()
            os.remove(temp_file)
            # print(f"Cleaned up chunk {chunk_id}")
    
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        raise
    finally:
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        print(f"Completed processing {file_path}")

def main():
    spark = init_spark()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relative_file_path = r"../collect_data/raw_data/shopeefood/2025-05-01/shopeefood_20250501_001_2000000_lines.json"
    file_path = os.path.normpath(os.path.join(script_dir, relative_file_path))
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    start_time = time.time()
    try:
        process_chunk(spark, file_path, chunk_size=250)
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time taken (with error): {elapsed_time:.2f} seconds")
        raise
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time taken: {elapsed_time:.2f} seconds")
        spark.stop()

if __name__ == "__main__":
    main()