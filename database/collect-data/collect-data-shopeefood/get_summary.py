import time
import requests

def get_summary(restaurantId=695027):
    url = "https://www.foody.vn/__get/Restaurant/GetSummary"
    timestamp = int(time.time() * 1000)
    params = {
        "t": timestamp,
        "ResId": restaurantId
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en,vi-VN;q=0.9,vi;q=0.8",
        "Referer": "https://www.foody.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.ok:
        data = response.json()
        return data
    print(f"Request failed with status code: {response.status_code}")
    return None
get_summary(1000045833)