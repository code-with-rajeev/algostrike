# helpers.py
import datetime

def normalize_data(data):
    """
    Normalize data to a scale of 0 to 1.
    Args:
        data (list): List of numerical values.
    
    Returns:
        list: Normalized data.
    """
    min_val = min(data)
    max_val = max(data)
    return [(x - min_val) / (max_val - min_val) for x in data]

def is_market_open():
    """
    Check if the market is open (Monday to Friday, 9:15 AM to 3:30 PM).
    Returns:
        bool: True if market is open, else False.
    """
    now = datetime.datetime.now()
    if now.weekday() >= 5:  # Saturday and Sunday
        return False
    return now.time() >= datetime.time(9, 15) and now.time() <= datetime.time(15, 30)