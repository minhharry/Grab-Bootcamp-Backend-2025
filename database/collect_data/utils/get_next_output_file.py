import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from datetime import datetime

def get_next_output_file(source):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_base_dir = os.path.join(script_dir, "..", "raw_data")
    date_str = datetime.now().strftime("%Y-%m-%d")
    local_dir = os.path.join(local_base_dir, source, date_str)
    os.makedirs(local_dir, exist_ok=True)
    existing_files = [f for f in os.listdir(local_dir) if f.startswith(f"{source}_{date_str.replace('-', '')}")]
    sequence = len(existing_files) + 1
    filename = f"{source}_{date_str.replace('-', '')}_{sequence:03d}.json"
    output_file_path = os.path.join(local_dir, filename)
    return output_file_path, str(sequence).zfill(3)