"""
Configuration
"""
ABOUT = {
    
    "name":"5_EMA_Nifty_Option_Selling",
    "type":"Demo",
    "author":"Rajeev"
    
    }
STATIC_REQUIREMENTS = [
#Testing: SUB, SNAP, API method of fetching data
    {
        "instrument":"NIFTY",
        "timeframe":"5M",
        "frequency":"SUB", #Live response
        "instrument_token":"26000",
        "exchange_segment":"nse_cm"
    }
]