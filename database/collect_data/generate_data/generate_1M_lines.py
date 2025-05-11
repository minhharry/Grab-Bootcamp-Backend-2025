import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

print("script_dir", script_dir)

# Trước tiên trong thư mục shopeefood/2025-05-01/ phải có file
# shopeefood_2025-05-01_001.json trước đã, từ đó script này sẽ nhân lên thành X triệu dòng
date_str = "2025-05-01"
crawl_id = "001"
source = "shopeefood"

# Nhân lên thành ... dòng
target_lines = 2_000_000

input_relative_path = f"../raw_data/{source}/{date_str}/{source}_{date_str.replace('-', '')}_{crawl_id}.json"
output_relative_path = f"../raw_data/{source}/{date_str}/{source}_{date_str.replace('-', '')}_{crawl_id}_{target_lines}_lines.json"
input_path = os.path.join(script_dir, input_relative_path)
output_path = os.path.join(script_dir, output_relative_path)
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Đọc dữ liệu đầu vào
with open(input_path, "r", encoding="utf-8") as infile:
    lines = [line.strip() for line in infile if line.strip()]

original_len = len(lines)
# Nếu file gốc đã lớn hơn hoặc bằng 100k dòng thì chỉ lấy 100k dòng đầu
if original_len >= target_lines:
    lines_to_write = lines[:target_lines]
else:
    times = target_lines // original_len
    remainder = target_lines % original_len
    lines_to_write = lines * times + lines[:remainder]

# Ghi ra file output
with open(output_path, "w", encoding="utf-8") as outfile:
    for line in lines_to_write:
        outfile.write(line + "\n")

print(f"✅ Đã ghi {len(lines_to_write)} dòng vào: {output_path}")