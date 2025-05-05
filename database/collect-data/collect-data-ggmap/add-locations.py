import json
import os
import requests

script_dir = os.path.dirname(os.path.abspath(__file__))

print("script_dir", script_dir)

input_relative_path = "data-without-locations/quan_an_tp_hcm_google_maps_selenium.jsonl"
# input_relative_path = "data-without-locations/mock-input.jsonl"
input_path = os.path.join(script_dir, input_relative_path)
output_path = os.path.join(script_dir, "../raw-data/googlemaps/googlemaps-restaurants-with-locations.jsonl")


API_KEY = "..." # gomaps.pro API key

def search_api(address):
    base_url = "https://maps.gomaps.pro/maps/api/place/textsearch/json"
    params = {
        "query": address,
        "radius": 1000,
        "language": "en",
        "region": "en",
        "key": API_KEY
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Tự động raise lỗi nếu status != 200
    return response.json().get("results", [])

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        if not line.strip():
            continue  # bỏ qua dòng trống
        obj = json.loads(line)
        address = obj.get("address", "")
        search_results = search_api(address)
        obj["search_results"] = search_results
        outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")

print("✅ Xử lý xong! File đã được ghi vào:")
print(output_path)


# with open(output_path, "r", encoding="utf-8") as f:
#     first_line = f.readline()
#     first_obj = json.loads(first_line)

# print("Schema:")
# for key, value in first_obj.items():
#     print(f"{key}: {type(value).__name__}")