# performance.py

def calculate_pnl(trades):
    """
    Calculate profit/loss from executed trades.
    Args:
        trades (list): A list of executed trade dictionaries.
                      Example: [{'entry': 100, 'exit': 105, 'size': 1}, ...]
    
    Returns:
        float: Net profit/loss
    """
    pnl = 0
    for trade in trades:
        pnl += (trade['exit'] - trade['entry']) * trade['size']
    return pnl

def evaluate_performance(trades):
    """
    Evaluate the algorithm's performance metrics.
    Args:
        trades (list): A list of executed trade dictionaries.
    
    Returns:
        dict: Performance metrics (PnL, win rate, etc.)
    """
    pnl = calculate_pnl(trades)
    wins = sum(1 for t in trades if t['exit'] > t['entry'])
    win_rate = wins / len(trades) if trades else 0

    return {
        'total_pnl': pnl,
        'win_rate': round(win_rate * 100, 2),
        'total_trades': len(trades)
    }