"""
This code demonstrates how to fetch data from an external API.
"""

import requests

API_ENDPOINT = "https://api.example.com/data"
API_KEY = "your_api_key"

def fetch_market_data(symbol):
    """
    Fetches market data for a given symbol from the external API.
    """
    try:
        response = requests.get(f"{API_ENDPOINT}?symbol={symbol}", headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Failed to fetch market data: {str(e)}")
        return None