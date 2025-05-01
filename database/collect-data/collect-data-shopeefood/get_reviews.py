import time
import requests

def extract_reviews(raw_data):
    items = raw_data.get("Items", [])
    extracted = []

    for review in items:
        extracted.append({
            "Title": review.get("Title", ""),
            "Description": review.get("Description", ""),
            "AvgRating": review.get("AvgRating", None),
            "Review_date": review.get("CreatedOnTimeDiff", None),
            "Author": review.get("Owner", None).get("DisplayName", ""),
        })

    return extracted

def get_reviews(restaurantId=695027):
    url = "https://www.foody.vn/__get/Review/ResLoadMore"
    timestamp = int(time.time() * 1000)
    params = {
        "t": timestamp,
        "ResId": restaurantId,
        "Count": "10",
        "Type": "1",
        "isLatest": "true"
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en,vi-VN;q=0.9,vi;q=0.8",
        "Origin": "https://www.foody.vn",
        "Referer": "https://www.foody.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.post(url, headers=headers, params=params)

    if response.ok:
        data = response.json()
        return extract_reviews(data)
    print(f"Request failed with status code: {response.status_code}")
    return None