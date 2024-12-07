# This file is just for demo purpose
from interfaces.data_provider import fetch_premarket_data

def analyze_premarket():
    """Fetch and analyze premarket data to decide trading focus."""
    data = fetch_premarket_data()
    indices_to_monitor = []
    for index, details in data.items():
        if details['gap_up'] or details['high_volume']:
            indices_to_monitor.append(index)
    return indices_to_monitor