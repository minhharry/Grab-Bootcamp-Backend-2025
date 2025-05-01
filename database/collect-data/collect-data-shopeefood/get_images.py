import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_images(driver):
    

    seen_items = set()
    
    images = []

    while True:
        driver.execute_script("window.scrollBy(0, 1000);") 
        time.sleep(2)

        item_rows = driver.find_elements(By.CLASS_NAME, "item-restaurant-row")
        new_item_found = False 

        for item in item_rows:
            try:
                name = item.find_element(By.XPATH, './/h2[@class="item-restaurant-name"]').text
            except:
                name = ''
            
            if name not in seen_items:
                seen_items.add(name)
                
                try:
                    current_price = item.find_element(By.XPATH, './/div[@class="col-auto product-price"]/div[@class="current-price"]').text
                except:
                    current_price = 'NA'

                # Xử lý ảnh
                try:
                    img_element = item.find_element(By.XPATH, './/div[contains(@class, "item-restaurant-img")]//img')
                    img_url = img_element.get_attribute('src')
                except Exception as e:
                    img_url = 'NA'

                new_item_found = True 
        images.append(
            {
                'name': name,
                'current_price': current_price,
                'img_url': img_url
            }
        )
        
        if not new_item_found:
            print("Không có phần tử mới, dừng lại.")
            break
            
    return images