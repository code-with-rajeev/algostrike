"""
Configuration
"""
ABOUT = {
    
    "name":"9_26_EMA_Crossover",
    "type":"Demo",
    "author":"Rajeev"
    
    }
STATIC_REQUIREMENTS = [
#Testing: SUB, SNAP, API method of fetching data
    {
        "instrument":"NIFTY",
        "timeframe":"1M",
        "frequency":"SUB", #Live response
        "instrument_token":"26000",
        "exchange_segment":"nse_cm"
    }
]