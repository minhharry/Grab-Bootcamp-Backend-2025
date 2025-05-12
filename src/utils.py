
from typing import Optional
from math import radians, sin, cos, sqrt, atan2

def extract_price_level(price_range: dict) -> Optional[int]:
    """
    Extracts the price level based on the price_max value in the price_range dictionary.
    Returns an integer representing the price level (1, 2, 3) or None if invalid.

    Args:
        price_range (dict): A dictionary containing 'price_min' and 'price_max'.

    Returns:
        Optional[int]: Price level (1, 2, 3) or None.
    """
    if not isinstance(price_range, dict):
        return None

    # Ensure that the price_range has 'price_max' key and it has a valid value
    price_max = price_range.get("price_max", None)
    if price_max is None:
        return None

    try:
        price_max = float(price_max)
        if price_max > 150000:
            return 3
        elif 50000 < price_max <= 150000:
            return 2
        elif price_max <= 50000:
            return 1
        return None
    except (ValueError, TypeError):
        return None
    



def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius = 6371  # Radius of the Earth in kilometers. Use 3956 for miles.

    return radius * c