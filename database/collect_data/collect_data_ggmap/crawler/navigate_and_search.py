from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import os
import random
from utils.delays import random_delay
from utils.scroll_handler import scroll_to_load_restaurants
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GoogleMapsNavigator:
    """Quản lý điều hướng và tìm kiếm trên Google Maps, tránh bị phát hiện là bot."""
    
    def __init__(self, browser_type="chrome", base_url="https://www.google.com.vn", use_proxy=False):
        """Khởi tạo trình duyệt với cấu hình chống phát hiện bot."""
        self.base_url = base_url
        self.use_proxy = use_proxy
        self.driver = self._initialize_browser(browser_type)
        self.wait = WebDriverWait(self.driver, 30)
    
    def _initialize_browser(self, browser_type):
        """Khởi tạo trình duyệt Selenium với các biện pháp chống phát hiện."""
        try:
            ua = UserAgent()
            user_agent = ua.chrome  # Tạo User-Agent ngẫu nhiên giống Chrome thực
            
            if browser_type.lower() == "chrome":
                options = Options()
                # Các tùy chọn để tránh phát hiện bot
                options.add_argument(f'--user-agent={user_agent}')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument('--start-maximized')
                options.add_argument('--disable-infobars')
                options.add_argument('--disable-notifications')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                # Tùy chọn proxy nếu bật
                if self.use_proxy:
                    proxy = self._get_random_proxy()
                    if proxy:
                        options.add_argument(f'--proxy-server={proxy}')
                
                driver = webdriver.Chrome(options=options)
                
                # Xóa thuộc tính navigator.webdriver
                driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                    'source': '''
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    '''
                })
                
                # Mô phỏng các thuộc tính trình duyệt thực
                driver.execute_cdp_cmd('Emulation.setUserAgentOverride', {
                    'userAgent': user_agent,
                    'platform': 'Windows NT 10.0; Win64; x64'
                })
                
            else:
                raise ValueError(f"Loại trình duyệt {browser_type} không được hỗ trợ")
            
            logging.info("Đã khởi tạo trình duyệt với cấu hình chống phát hiện")
            return driver
        except Exception as e:
            logging.error(f"Lỗi khi khởi tạo trình duyệt: {str(e)}")
            raise
    
    def _get_random_proxy(self):
        """Lấy proxy ngẫu nhiên từ danh sách hoặc dịch vụ proxy."""
        
        proxy_list = []
        return random.choice(proxy_list) if proxy_list else None
    
    def _wait_for_page_load(self):
        """Chờ trang tải hoàn tất."""
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    
    def _find_search_box(self, selectors, description="ô tìm kiếm"):
        """Tìm ô tìm kiếm với nhiều selector thay thế."""
        for selector, by in selectors:
            try:
                search_box = self.wait.until(EC.presence_of_element_located((by, selector)))
                logging.info(f"Đã tìm thấy {description}")
                return search_box
            except:
                logging.warning(f"Không tìm thấy {description} với selector {selector}")
        raise Exception(f"Không tìm thấy {description}")
    
    def _click_link(self, selectors, description="liên kết"):
        """Nhấp vào liên kết với nhiều selector thay thế."""
        for selector, by in selectors:
            try:
                link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                link.click()
                logging.info(f"Đã nhấp vào {description}")
                return True
            except:
                logging.warning(f"Không tìm thấy {description} với selector {selector}")
        raise Exception(f"Không tìm thấy {description}")
    
    def navigate_to_google_maps(self):
        """Điều hướng đến Google Maps."""
        try:
            logging.info("Đang mở Google...")
            self.driver.get(self.base_url)
            random_delay(6, 10)
            self._wait_for_page_load()
            
            # Tìm ô tìm kiếm trên Google
            selectors = [
                ("q", By.NAME),
                ("input[title='Search']", By.CSS_SELECTOR)
            ]
            search_box = self._find_search_box(selectors, "ô tìm kiếm Google")
            
            # Tìm kiếm "google map"
            search_box.send_keys("google map")
            search_box.send_keys(Keys.ENTER)
            random_delay(5, 10)
            self._wait_for_page_load()
            
            # Nhấp vào liên kết Google Maps
            selectors = [
                ("//a[contains(@href, 'maps.google')]", By.XPATH),
                ("a[href*='maps.google']", By.CSS_SELECTOR)
            ]
            self._click_link(selectors, "liên kết Google Maps")
            random_delay(5, 10)
            self._wait_for_page_load()
            
            return True
        except Exception as e:
            logging.error(f"Lỗi khi điều hướng đến Google Maps: {str(e)}")
            with open("navigation_error.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            return True
    
    def search_restaurants(self, query):
        """Tìm kiếm nhà hàng trên Google Maps."""
        try:
            # Tìm ô tìm kiếm trên Google Maps
            selectors = [
                ("input.searchboxinput", By.CSS_SELECTOR),
                ("input[aria-label='Tìm kiếm trên Google Maps']", By.CSS_SELECTOR),
                ("//div[@id='searchbox']//input[@role='combobox']", By.XPATH)
            ]
            search_box = self._find_search_box(selectors, "ô tìm kiếm Google Maps")
            
            # Tìm kiếm nhà hàng
            search_box.send_keys(query)
            search_box.send_keys(Keys.ENTER)
            random_delay(5, 28)
            logging.info(f"Đã tìm kiếm: {query}")
            
            # Chờ danh sách nhà hàng
            self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Nv2PK")))
            
            # Cuộn trang để tải thêm nhà hàng
            logging.info("Đang cuộn trang để tải thêm nhà hàng...")
            restaurants = scroll_to_load_restaurants(self.driver, target_count=50, max_scrolls=20)
            logging.info(f"Đã tải {len(restaurants)} nhà hàng")
            
            return restaurants
        except Exception as e:
            logging.error(f"Lỗi khi tìm kiếm nhà hàng: {str(e)}")
            with open("search_error.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            return []
    
    def get_driver(self):
        """Trả về đối tượng driver để sử dụng ở các bước tiếp theo."""
        return self.driver
    
    def close(self):
        """Đóng trình duyệt."""
        try:
            self.driver.quit()
            logging.info("Đã đóng trình duyệt")
        except Exception as e:
            logging.error(f"Lỗi khi đóng trình duyệt: {str(e)}")

def navigate_and_search(search_query):
    """Hàm chính để điều hướng và tìm kiếm (tương thích với mã gốc)."""
    navigator = GoogleMapsNavigator(use_proxy=False)  # Bật proxy nếu cần
    try:
        if not navigator.navigate_to_google_maps():
            return []
        return navigator.search_restaurants(search_query), navigator.get_driver()
    except Exception as e:
        logging.error(f"Lỗi trong quá trình điều hướng và tìm kiếm: {str(e)}")
        return [], None
    finally:
        # Đừng đóng trình duyệt ở đây để crawl_and_save có thể sử dụng
        pass