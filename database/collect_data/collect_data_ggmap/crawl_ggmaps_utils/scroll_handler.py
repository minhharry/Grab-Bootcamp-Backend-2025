from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils.delays import random_delay
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scroll_to_load_restaurants(driver, target_count=20, max_scrolls=4):
    """Cuộn trang để tải danh sách nhà hàng."""
    scroll_pause_time = random.uniform(2, 5)
    for _ in range(max_scrolls):
        restaurants = driver.find_elements(By.CLASS_NAME, "Nv2PK")
        if len(restaurants) >= target_count:
            logging.info(f"Đã tải đủ {len(restaurants)} nhà hàng")
            return restaurants[:target_count]
        
        if restaurants:
            driver.execute_script("arguments[0].scrollIntoView();", restaurants[-1])
        else:
            driver.execute_script("window.scrollBy(0, 1000);")
        random_delay(scroll_pause_time, scroll_pause_time + 2)
        
        try:
            WebDriverWait(driver, 5).until(
                lambda d: len(d.find_elements(By.CLASS_NAME, "Nv2PK")) > len(restaurants)
            )
        except:
            logging.warning("Không tải được thêm nhà hàng mới")
            break
    return driver.find_elements(By.CLASS_NAME, "Nv2PK")[:target_count]