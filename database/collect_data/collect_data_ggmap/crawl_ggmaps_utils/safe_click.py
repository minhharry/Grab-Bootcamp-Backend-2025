from selenium.common.exceptions import StaleElementReferenceException
from utils.delays import random_delay
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_click(element, driver, max_attempts=3):
    """Nhấp an toàn vào phần tử, xử lý lỗi StaleElementReferenceException."""
    for attempt in range(max_attempts):
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            return True
        except StaleElementReferenceException:
            logging.warning("Phần tử stale, thử lại...")
            random_delay(2, 8)
            continue
    logging.error("Không thể nhấp vào phần tử sau nhiều lần thử")
    return False