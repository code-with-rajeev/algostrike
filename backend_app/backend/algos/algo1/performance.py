# To demonstrate the purpose of this file.
from core.database import fetch_user_trades, update_algo_performance

def calculate_algo_performance(algo_id):
    """Calculate and update performance of an algorithm."""
    trades = fetch_user_trades(algo_id)
    profit_loss = sum([trade['profit'] for trade in trades])
    update_algo_performance(algo_id, profit_loss)
    return profit_loss