from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.delays import random_delay
from utils.safe_click import safe_click
from utils.add_locations import mock_get_location
import datetime
import json
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crawl_and_save_restaurant(driver, restaurant, output_file_path, crawl_id):
    """Thu thập dữ liệu chi tiết của một nhà hàng và lưu vào file."""
    try:
        name = restaurant.find_element(By.CLASS_NAME, "qBF1Pd").text.strip()
        logging.info(f"Đang xử lý quán: {name}")
        
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
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", restaurant)
        random_delay(7, 30)
        
        restaurant.click()
        random_delay(5, 32)
        
        try:
            avatar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button.aoRNLd.kn2E5e.NMjTrf.lvtCsd img'))
            )
            avatar_url = avatar.get_attribute("src")
        except:
            avatar_url = "N/A"
        
        try:
            address = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.Io6YTe"))
            ).text.strip()
        except:
            address = "N/A"
        
        reviews = []
        try:
            review_section = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.m6QErb.Pf6ghf.XiKgde.KoSBEe"))
            )
            driver.execute_script("arguments[0].scrollIntoView();", review_section)
            random_delay(10, 28)
            
            review_elements = driver.find_elements(By.CSS_SELECTOR, "div.jftiEf")[:5]
            for review in review_elements:
                try:
                    review_date = review.find_element(By.CSS_SELECTOR, "span.rsqaWe").text.strip()
                    review_author = review.find_element(By.CSS_SELECTOR, "div.d4r55").text.strip()
                    rating = review.find_element(By.CSS_SELECTOR, "span.kvMYJc").get_attribute("aria-label").strip()
                    try:
                        more_buttons = review.find_elements(By.CSS_SELECTOR, "button.w8nwRe.kyuRq")
                        if more_buttons:
                            if not safe_click(more_buttons[0], driver):
                                logging.warning("Không thể nhấp vào nút 'Xem thêm'")
                                continue
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "span.wiI7pd:not(:empty)"))
                            )
                        text = review.find_element(By.CSS_SELECTOR, "span.wiI7pd").text.strip()
                    except:
                        text = "N/A"
                    
                    review_photos = []
                    photo_elements = review.find_elements(By.CSS_SELECTOR, "button.Tya61d")
                    for idx, photo in enumerate(photo_elements):
                        style = photo.get_attribute("style")
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
        location = mock_get_location(address)
        
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
            "crawl_time": crawl_time,
            "crawl_id": crawl_id,
            "search_results": location
        }
        
        try:
            with open(output_file_path, "a", encoding="utf-8") as f:
                json.dump(restaurant_data, f, ensure_ascii=False)
                f.write("\n")
            logging.info(f"Đã lưu dữ liệu quán {name} vào {output_file_path}")
        except Exception as e:
            logging.error(f"Lỗi khi lưu dữ liệu quán {name} vào {output_file_path}: {str(e)}")
        
        return restaurant_data
    except Exception as e:
        logging.error(f"Lỗi khi thu thập dữ liệu quán {name}: {str(e)}")
        return None