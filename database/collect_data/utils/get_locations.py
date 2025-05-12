import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_location(address):
    base_url = "https://maps.gomaps.pro/maps/api/place/textsearch/json"
    params = {
        "query": address,
        "radius": 1000,
        "language": "en",
        "region": "en",
        "key": os.getenv("GOMAPS_API_KEY")
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error for address '{address}': {e}")
        print(f"Response content: {response.text}")
        return []
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error for address '{address}': {e}")
        print(f"Response content: {response.text}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request Error for address '{address}': {e}")
        return []

def mock_get_location(address):
    # Giả lập dữ liệu địa chỉ cho mục đích thử nghiệm
    return [
        {
            "formatted_address": "136-9D Đ. Lê Thánh Tôn, Phường Bến Thành, Quận 1, Hồ Chí Minh, Vietnam",
            "geometry": {
                "location": {"lat": 10.7736855, "lng": 106.6981425},
                "viewport": {
                    "northeast": {"lat": 10.77504427989272, "lng": 106.6995057798927},
                    "southwest": {"lat": 10.77234462010728, "lng": 106.6968061201073}
                }
            },
            "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/geocode-71.png",
            "icon_background_color": "#7B9EB0",
            "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet",
            "name": "136-9D Đ. Lê Thánh Tôn",
            "place_id": "ChIJY2k_xjgvdTER6q7-oxEOm9o",
            "reference": "ChIJY2k_xjgvdTER6q7-oxEOm9o",
            "types": ["subpremise"]
        }
    ]


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("script_dir", script_dir)

    date_str = "2025-05-11"
    crawl_id = "003"
    input_relative_path = f"../raw_data/googlemaps/{date_str}/googlemaps_{date_str.replace('-', '')}_{crawl_id}.json"
    output_relative_path = f"../raw_data/added_locations_googlemaps/{date_str}/googlemaps_{date_str.replace('-', '')}_{crawl_id}_processed.json"
    input_path = os.path.join(script_dir, input_relative_path)
    output_path = os.path.join(script_dir, output_relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            if not line.strip():
                continue  # bỏ qua dòng trống
            obj = json.loads(line)
            address = obj.get("address", "")
            search_results = get_location(address)
            obj["search_results"] = search_results
            outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print("✅ Xử lý xong! File đã được ghi vào:")
    print(output_path)