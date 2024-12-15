# helper.py

# Dictionary to store required fields for each broker
BROKER_FIELDS = {
    'kotak_neo': ['customer_key', 'customer_secret', 'password', 'mobile_number'],
    'zerodha': ['api_key', 'api_secret', 'pin'],
    'angel_broking': ['client_id', 'password', 'api_key'],
    'dhan': ['client_id', 'password', 'api_key'],
    'upstox': ['client_id', 'password', 'api_key'],
    'fyers': ['client_id', 'password', 'api_key'],
    # Add more brokers here as needed
}

def get_required_fields(broker_name):
    """
    Returns the required fields for a specific broker.
    """
    return BROKER_FIELDS.get(broker_name, [])

def validate_broker_credentials(broker_name, credentials):
    """
    Validates if all required fields for the broker are provided.
    """

def log_debug(message):
    """
    Simple logging function to print debug messages.
    """
    print(f"[DEBUG] {message}")

# Add other utility functions as needed
