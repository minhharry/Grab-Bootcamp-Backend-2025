import time
import random

def random_delay(min_seconds=2, max_seconds=5):
    """Thêm thời gian chờ ngẫu nhiên."""
    time.sleep(random.uniform(min_seconds, max_seconds))