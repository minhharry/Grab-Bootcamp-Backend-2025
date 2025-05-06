from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from get_images import get_images
from get_reviews import get_reviews
from get_restaurants import get_list_place
from get_summary import get_summary

import os
import json
import datetime
import time


driver = webdriver.Edge()
driver.delete_all_cookies()
driver.maximize_window()


script_dir = os.path.dirname(os.path.abspath(__file__))
input_relative_path = "../raw-data/shopeefood/data-shopee-food.jsonl"

output_file = os.path.join(script_dir, input_relative_path)

if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)

list_places = get_list_place(200)
# print(list_places)

for place in list_places:    
    try:
        restaurant = get_summary(place['Id']).get('Restaurant', {})
        avgReview = get_summary(place['Id']).get('AvgReview', {})
    except Exception as e:
        print(f"Lỗi khi lấy thông tin quán: {e}")
        continue
    
    try:
        reviews = get_reviews(place['Id'])
    except Exception as e:
        print(f"Lỗi khi lấy đánh giá quán: {e}")
        continue
    
    driver.get(place['shop_url'])
    
    print(f"Đang lấy thông tin quán: {restaurant.get('Name', '')}")
    
    try:
        avatar_url = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.detail-restaurant-img img'))
        ).get_attribute('src')
    except:
        avatar_url = 'N/A'
        print("Không tìm thấy ảnh đại diện quán, gán là 'N/A'")
        
    try:
        restaurant_type = driver.find_element(By.CSS_SELECTOR, 'div.kind-restaurant span').text
    except:
        restaurant_type = 'N/A'  
        print("Không tìm thấy loại hình quán, gán là 'N/A'")  
    
    try:
        price_range = driver.find_element(By.CSS_SELECTOR, 'div.cost-restaurant').text
    except:
        price_range = 'N/A'
        print("Không tìm thấy khoảng giá, gán là 'N/A'")
        
    try:
        opening_hours = driver.find_element(By.CSS_SELECTOR, 'div.time').text
    except:
        opening_hours = 'N/A'
        print("Không tìm thấy giờ mở cửa, gán là 'N/A'")    
    
    try:
        images = get_images(driver)
    except Exception as e:
        print(f"Lỗi khi lấy ảnh quán: {e}")
        continue
    
    crawl_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crawl_id = datetime.datetime.now().strftime("%Y-%m-%d") + str("-001") 
    name = restaurant.get("Name", "")
    longitude = place['longitude']
    latitude = place['latitude']
    
    restaurant_data = {"name": name,
                "restaurant_type": restaurant_type,
                "avatar_url": avatar_url,
                "price_range": price_range,
                "opening_hours": opening_hours,
                "address": restaurant.get("Address", ""),
                "longitude": longitude,
                "latitude": latitude,
                "avgRating": restaurant.get("AvgRating", None),
                "rating_count": avgReview.get("Total", 0),
                "source": "ShopeeFood",
                "reviews": reviews,
                "images": images,
                "restaurant_url": place["shop_url"], 
                
                "crawl_time": crawl_time,
                "crawl_id": crawl_id,
                "source_unique_id": place['Id']
                }

    try:
        with open(output_file, "a", encoding="utf-8") as f:
            json.dump(restaurant_data, f, ensure_ascii=False)
            f.write("\n")
        print(f"Đã lưu dữ liệu quán {name} vào {output_file}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu quán {name} vào {output_file}: {e}")
        
driver.quit()
