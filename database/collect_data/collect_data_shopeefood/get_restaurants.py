import time
import requests

def extract_shopURL_and_ID(list_place):
    result = []
    for item in list_place['Items']:
        shop_url = 'https://shopeefood.vn' + item.get('Url', '')
        shop_id = int(item.get('Id'))
        latitude = float(item.get('Latitude'))
        longitude = float(item.get('Longitude'))
        
        result.append({
            'Id': shop_id,
            'shop_url': shop_url,
            'latitude': latitude,
            'longitude': longitude
        })
        
    return result

def get_list_place(count = 5, page=1):
    url = "https://www.foody.vn/__get/Place/HomeListPlace"
    timestamp = int(time.time() * 1000)
    page = 1
    params = {
        "t": timestamp,
        "page": page,
        "lat": "10.823099",
        "lon": "106.629664",
        "count": str(count),
        "type": "1"
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en,vi-VN;q=0.9,vi;q=0.8",
        "Referer": "https://www.foody.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    cookies = {
        "flg": "vn",
        "floc": "217", # TPHCM
        "gcat": "food", # food
    }

    response = requests.get(url, headers=headers, params=params, cookies=cookies)
    if response.ok:
        data = response.json()
        return extract_shopURL_and_ID(data)
    print(f"Request failed with status code: {response.status_code}")
    return None