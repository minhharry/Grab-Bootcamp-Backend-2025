from crawler.navigate_and_search import navigate_and_search
from crawler.crawl_and_save import crawl_and_save_restaurant
from utils.get_next_output_file import get_next_output_file
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Lấy file đầu ra
    output_file_path, crawl_id = get_next_output_file("googlemaps")
    
    # Danh sách truy vấn tìm kiếm
    search_keys = [
        "restaurants in district 1 Ho Chi Minh City",
        "Món chay thành phố Hồ Chí Minh",
        "Quán ăn ở quận 2 Thành phố Hồ Chí Minh",
        "Nhà hàng ở quận 3 TP HCM",
        "Quán ăn ngon ở quận 4 TP HCM",
        "Đồ ăn ở quận 5 TP HCM",
        "Ẩm thực quận 6 TP HCM",
        "foods in district 2 ho chi minh city",
    ]
    
    # Điều hướng và tìm kiếm nhà hàng
    restaurants, driver = navigate_and_search(search_keys[0])
    if not restaurants or not driver:
        logging.error("Không tìm thấy nhà hàng nào hoặc driver không khởi tạo")
        return
    
    try:
        # Thu thập và lưu dữ liệu từng nhà hàng
        for restaurant in restaurants:
            crawl_and_save_restaurant(driver, restaurant, output_file_path, crawl_id)
    finally:
        # Đóng trình duyệt
        if driver:
            try:
                driver.quit()
                logging.info("Đã đóng trình duyệt")
            except Exception as e:
                logging.error(f"Lỗi khi đóng trình duyệt: {str(e)}")

if __name__ == "__main__":
    main()