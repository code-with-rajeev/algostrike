from redis_test import update
from sample import make_connection
import threading
print("Starting First algo")
mapping = {
    '55631': "NIFTY25FEB22800CE",
    '55632': "NIFTY25FEB22800PE",
    '26000': "NIFTY"
    }

instrument_tokens = [{"instrument_token": "26000", "exchange_segment": "nse_fo"}]

# Connect
client = make_connection()
def on_message(message):
    pass
def on_error(error_message):
    print("error is ",error_message)
# Handle socket
client.on_message = on_message
client.on_error = on_error

def socket():
    client.subscribe(instrument_tokens=[{"instrument_token": "26000", "exchange_segment": "nse_cm"}], isIndex=False,isDepth=False)
threading.Thread(target=socket).start()

# Start Live Stream
client.subscribe(instrument_tokens=instrument_tokens, isIndex=False,isDepth=False)

