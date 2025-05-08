import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# script_dir = os.path.dirname(os.path.abspath(__file__))

# print("script_dir", script_dir)

# input_relative_path = "../../raw_data/googlemaps/2025-05-07/googlemaps_20250507_001.json"
# input_path = os.path.join(script_dir, input_relative_path)
# output_path = os.path.join(script_dir, "googlemaps_20250507_001.json")

def get_location(address):
    base_url = "https://maps.gomaps.pro/maps/api/place/textsearch/json"
    params = {
        "query": address,
        "radius": 1000,
        "language": "en",
        "region": "en",
        "key": os.getenv("GOMAPS_API_KEY") # gomaps.pro API key đăng ký miễn phí tại https://gomaps.pro/

    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Tự động raise lỗi nếu status != 200
    return response.json().get("results", [])

def mock_get_location(address):
    # Giả lập dữ liệu địa chỉ cho mục đích thử nghiệm
    return [{"formatted_address": "136-9D Đ. Lê Thánh Tôn, Phường Bến Thành, Quận 1, Hồ Chí Minh, Vietnam", "geometry": {"location": {"lat": 10.7736855, "lng": 106.6981425}, "viewport": {"northeast": {"lat": 10.77504427989272, "lng": 106.6995057798927}, "southwest": {"lat": 10.77234462010728, "lng": 106.6968061201073}}}, "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/geocode-71.png", "icon_background_color": "#7B9EB0", "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet", "name": "136-9D Đ. Lê Thánh Tôn", "place_id": "ChIJY2k_xjgvdTER6q7-oxEOm9o", "reference": "ChIJY2k_xjgvdTER6q7-oxEOm9o", "types": ["subpremise"]}]

# with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
#     for line in infile:
#         if not line.strip():
#             continue  # bỏ qua dòng trống
#         obj = json.loads(line)
#         address = obj.get("address", "")
#         search_results = mock_get_location(address)
#         obj["search_results"] = search_results
#         outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")

# print("✅ Xử lý xong! File đã được ghi vào:")
# print(output_path)