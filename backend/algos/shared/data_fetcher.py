# This file is just for demo purpose
from interfaces.data_provider import fetch_live_data, fetch_historical_data

def get_live_data(index):
    """Fetch live market data for the given index."""
    return fetch_live_data(index)

def get_historical_data(index, start_date, end_date):
    """Fetch historical data for the given index within the date range."""
    return fetch_historical_data(index, start_date, end_date)