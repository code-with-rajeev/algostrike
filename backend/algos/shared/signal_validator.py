# This file is just for demo purpose
from shared.constants import BUY, SELL

def validate_signal(signal):
    """Validate if a signal is strong enough to act on."""
    if signal in [BUY, SELL]:
        return True
    return False