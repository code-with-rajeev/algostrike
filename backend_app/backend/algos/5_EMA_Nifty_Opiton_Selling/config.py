"""
Configuration
"""
ABOUT = {
    
    "name":"5_EMA_Nifty_Option_Selling",
    "type":"Demo",
    "author":"Rajeev"
    
    }
STATIC_REQUIREMENTS = [
    """
    Testing: SUB, SNAP, API method of fetching data
    """
    {
        "instrument":"NIFTY",
        "timeframe":"1M",
        "frequncy":"SUB" #Live response
    },
    
    {
        "instrument":"RELIANCE",
        "timeframe":"2M",
        "frequency":"SNAP" #Minor Delay Response
    },
    
    {
        "instrument":"ZOMATO",
        "timeframe":"5M",
        "frequency":"API" #Major Delay Response
    }
]
