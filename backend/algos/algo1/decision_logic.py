# decision_logic.py
# Note: This logic is just temporary.
import numpy as np

def generate_signal(market_data):
    """
    Core decision logic to generate a trade signal.
    Args:
        market_data (dict): A dictionary containing price, volume, and other data.
    
    Returns:
        str: "BUY", "SELL", or "HOLD"
    """
    prices = market_data['close_prices']
    short_ma = np.mean(prices[-10:])  # 10-period moving average
    long_ma = np.mean(prices[-50:])  # 50-period moving average

    if short_ma > long_ma:
        return "BUY"
    elif short_ma < long_ma:
        return "SELL"
    return "HOLD"