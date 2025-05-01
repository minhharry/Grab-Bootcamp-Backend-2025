from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import datetime
import json
import pandas as pd
import time
import random
import requests
import os
import re

# Hàm thêm thời gian chờ ngẫu nhiên
def random_delay(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))
    
def safe_click(element, driver, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            return True
        except StaleElementReferenceException:
            print("Phần tử stale, thử lại...")
            random_delay(2, 8)
            continue
    return False

def scroll_to_load_restaurants(driver, target_count=20, max_scrolls=4):
    scroll_pause_time = random.uniform(2, 5)
    for _ in range(max_scrolls):
        restaurants = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        if len(restaurants) >= target_count:
            print(f"Đã tải đủ {len(restaurants)} nhà hàng")
            return restaurants[:target_count]
        
        # Cuộn đến phần tử cuối cùng hoặc cuộn xuống
        if restaurants:
            driver.execute_script("arguments[0].scrollIntoView();", restaurants[-1])
        else:
            driver.execute_script("window.scrollBy(0, 1000);")
        random_delay(scroll_pause_time, scroll_pause_time + 2)
        
        # Chờ thêm phần tử mới
        try:
            WebDriverWait(driver, 5).until(
                lambda d: len(d.find_elements(By.CLASS_NAME, "Nv2PK")) > len(restaurants)
            )
        except:
            print("Không tải được thêm nhà hàng mới")
            break
    return driver.find_elements(By.CLASS_NAME, "Nv2PK")[:target_count]
    
output_file = "../raw-data/googlemaps/quan_an_tp_hcm_google_maps_selenium.jsonl"
if not os.path.exists(output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)


driver = webdriver.Edge()
driver.delete_all_cookies()
driver.maximize_window()

# Tạo thư mục lưu ảnh
if not os.path.exists("review_images"):
    os.makedirs("review_images")

try:
    # Truy cập Google Maps
    print("Đang mở Google...")
    driver.get("https://www.google.com")
    random_delay(6, 10)

    # Chờ JavaScript tải xong
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    
    print("Đang tìm ô tìm kiếm...")
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
    except:
        print("Không tìm thấy ô tìm kiếm với name='q'. Thử selector thay thế...")
        try:
            search_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[title='Search']"))
            )
        except:
            print("Không tìm thấy ô tìm kiếm. In HTML để kiểm tra...")
            with open("google_page.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.quit()
            exit()

    # Nhập "google map" và tìm kiếm
    search_box.send_keys("google map")
    search_box.send_keys(Keys.ENTER)
    random_delay(5, 10)
    print("Đã tìm kiếm 'google map'")

    # Chờ kết quả tìm kiếm tải
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Tìm và nhấp vào liên kết Google Maps
    print("Đang tìm liên kết Google Maps...")
    try:
        maps_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'maps.google')]"))
        )
        maps_link.click()
        random_delay(5, 10)
        print("Đã nhấp vào liên kết Google Maps")
    except:
        print("Không tìm thấy liên kết Google Maps. Thử selector thay thế...")
        try:
            maps_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='maps.google']"))
            )
            maps_link.click()
            random_delay(5, 10)
            print("Đã nhấp vào liên kết Google Maps")
        except:
            print("Không tìm thấy liên kết Google Maps. In HTML để kiểm tra...")
            with open("search_results.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.quit()
            exit()

    # Chờ Google Maps tải
    print("Đang chờ Google Maps tải...")
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # Chờ và tìm ô tìm kiếm
    try:
        print("Đang tìm ô tìm kiếm...")
        # Thử selector chính: class="searchboxinput"
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.searchboxinput"))
        )
    except:
        print("Không tìm thấy ô tìm kiếm với class='searchboxinput'. Thử selector thay thế...")
        try:
            # Thử selector thay thế: aria-label
            search_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Tìm kiếm trên Google Maps']"))
            )
        except:
            print("Không tìm thấy ô tìm kiếm với aria-label='Tìm kiếm trên Google Maps'. Thử selector thay thế khác...")
            try:
                # Thử selector thay thế: trong div id="searchbox"
                search_box = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='searchbox']//input[@role='combobox']"))
                )
            except:
                print("Không tìm thấy ô tìm kiếm. In HTML để kiểm tra...")
                with open("page.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                driver.quit()
                exit()

    # Gửi truy vấn tìm kiếm
    search_keys = ["restaurants in district 1 Ho Chi Minh City",
                   "Món chay thành phố Hồ Chí Minh",
                   "Quán ăn ở quận 2 Thành phố Hồ Chí Minh",
                   "Nhà hàng ở quận 3 TP HCM",
                   "Quán ăn ngon ở quận 4 TP HCM",
                   "Đồ ăn ở quận 5 TP HCM",
                   "Ẩm thực quận 6 TP HCM",
                   "foods in district 2 ho chi minh city",]
    search_box.send_keys(search_keys[0])
    search_box.send_keys(Keys.ENTER)
    random_delay(5, 28)
    print("Đã tìm kiếm quán ăn")

    # Chờ đợi các đối tượng Nv2PK liên quan tới kết quả tìm kiếm địa điểm đã được load
    # Mỗi đối tượng Nv2PK đại diện cho một quán ăn
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Nv2PK"))
    )

    # # Danh sách lưu dữ liệu
    # data = []
    
        # Chờ các phần tử Nv2PK ban đầu
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "Nv2PK"))
    )

    # Cuộn trang để tải thêm nhà hàng
    print("Đang cuộn trang để tải thêm nhà hàng...")
    target_count = 50  # Số nhà hàng mong muốn
    max_scrolls = 20  # Giới hạn số lần cuộn để tránh vòng lặp vô hạn

    restaurants = scroll_to_load_restaurants(driver, target_count, max_scrolls)
    for index, restaurant in enumerate(restaurants):
        print("len(restaurants) ", len(restaurants))
        try:
            # Lấy tên quán bằng cách lấy text từ đối tượng "qBF1Pd" nằm trong đối tượng Nv2PK
            name = restaurant.find_element(By.CLASS_NAME, "qBF1Pd").text.strip()
            print(f"Đang xử lý quán: {name}")
            
            rating_element = restaurant.find_element(By.CLASS_NAME, "MW4etd")
            restaurant_rating = rating_element.text.strip() if rating_element.text else "N/A"

            count_element = restaurant.find_element(By.CLASS_NAME, "UY7F9")
            restaurant_rating_count = count_element.text.strip("()") if count_element.text else "N/A"
            
            try:
                price_element = restaurant.find_element(By.CSS_SELECTOR, "div.W4Efsd div.AJB7ye span:nth-child(3) span:last-child")
                price_range = price_element.text.strip() if price_element.text else "N/A"
            except:
                price_range = "N/A"
            
            try:
                full_status = restaurant.find_element(
                    By.CSS_SELECTOR, "div.W4Efsd > div.W4Efsd:nth-of-type(2) span"
                ).text.strip()

                # Tách theo dấu "⋅"
                parts = [part.strip() for part in full_status.split("⋅")]

                open_status = parts[0] if len(parts) > 0 else "N/A"
                closing_time = " ⋅ ".join(parts[1:]) if len(parts) > 1 else "N/A"
            except:
                open_status = "N/A"
                closing_time = "N/A"

            
            try:
                restaurant_type_element = restaurant.find_element(By.CSS_SELECTOR, "div.W4Efsd > div.W4Efsd span span")
                restaurant_type = restaurant_type_element.text.strip()
            except:
                restaurant_type = "N/A"
            
            # Cuộn đến quán
            # arguments[0] đại diện cho biên số đầu tiên được truyền vào hàm
            # ở đây là đối tượng restaurant
            driver.execute_script("arguments[0].scrollIntoView();", restaurant)
            random_delay(7, 30)

            # Nhấp vào quán
            restaurant.click()
            # if not safe_click(restaurant, driver):
            #     print(f"Không thể nhấp vào quán {name}")
            #     continue
            random_delay(5, 32)
            
            try:
                avatar = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        'button.aoRNLd.kn2E5e.NMjTrf.lvtCsd img'
                    ))
                )
                
                avatar_url = avatar.get_attribute("src")
            except:
                avatar_url = "N/A"

            # Lấy địa chỉ
            try:
                # Nếu như nhà hàng đó có địa chỉ thì Io6YTe sẽ có text
                # By.CSS_SELECTOR và div.Io6YTe có nghĩa cuộn đến thẻ div có class là Io6YTe
                # để thẻ đó xuất hiện trong viewport (khung nhìn) để có thể click được.
                
                # vì trong giao diện của google maps có nhiều thẻ div có class là Io6YTe
                # dòng code này tìm thẻ div đầu tiên có class là Io6YTe, đó chính là địa chỉ
                address = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.Io6YTe"))
                ).text.strip()
            except:
                address = "N/A"

            # Lấy đánh giá và ảnh trong đánh giá
            reviews = []
            try:
                # cuộn tới thẻ <div> đầu tiên có cả bốn class m6QErb, Pf6ghf, XiKgde, và KoSBEe
                # đây chính là thẻ đánh dấu sắp tới các bài đánh giá
                # mục đích là để các bài đánh giá xuất hiện trong viewport (khung nhìn) để có thể click được
                review_section = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.m6QErb.Pf6ghf.XiKgde.KoSBEe"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", review_section)
                random_delay(10, 28)

                # mỗi thẻ <div> có class là jftiEf là một bài đánh giá
                review_elements = driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")[:5]
                for review in review_elements:
                    try:
                        # Lấy thông tin bài đánh giá
                        review_date = review.find_element(By.CSS_SELECTOR, "span.rsqaWe").text.strip()
                        review_author = review.find_element(By.CSS_SELECTOR, "div.d4r55").text.strip()
                        rating = review.find_element(By.CSS_SELECTOR, "span.kvMYJc").get_attribute("aria-label").strip()
                        try:
                            more_buttons = review.find_elements(By.CSS_SELECTOR, "button.w8nwRe.kyuRq")
                            if more_buttons:
                                if not safe_click(more_buttons[0], driver):
                                    print("Không thể nhấp vào nút 'Xem thêm'")
                                    continue
                                WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.wiI7pd:not(:empty)"))
                                )
                            text = review.find_element(By.CSS_SELECTOR, "span.wiI7pd").text.strip()
                        except:
                            text = "N/A"

                        # Lấy ảnh trong bài đánh giá
                        review_photos = []
                        review_id = review.get_attribute("data-review-id")
                        photo_elements = review.find_elements(By.CSS_SELECTOR, "button.Tya61d")
                        for idx, photo in enumerate(photo_elements):
                            style = photo.get_attribute("style")
                            # Trích xuất URL từ style
                            url_match = re.search(r'url\("(.+?)"\)', style)
                            if url_match:
                                photo_url = url_match.group(1)
                                review_photos.append(photo_url)
                                
                        reviews.append({
                            "review_author": review_author,
                            "review_date": review_date,
                            "rating": rating,
                            "text": text,
                            "photos": review_photos
                        })
                    except:
                        continue
            except:
                reviews = ["N/A"]

            crawl_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            restaurant_data = {
                "name": name,
                "avatar_url": avatar_url,
                "restaurant_type": restaurant_type,
                "open_status": open_status,
                "closing_time": closing_time,
                "price_range": price_range,
                "address": address,
                "restaurant_rating": restaurant_rating,
                "restaurant_rating_count": restaurant_rating_count,
                "reviews": reviews,
                "source": "GoogleMaps",
                "crawl_time": crawl_time
            }
            
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    json.dump(restaurant_data, f, ensure_ascii=False)
                    f.write("\n")
                print(f"Đã lưu dữ liệu quán {name} vào {output_file}")
            except Exception as e:
                print(f"Lỗi khi lưu dữ liệu quán {name} vào {output_file}: {e}")

        except Exception as e:
            print(f"Lỗi tại quán {name}: {e}")
            continue

finally:
    driver.quit()