from redis_test import update
from sample import make_connection
import threading
print("Starting First algo")
mapping = {
    '55631': "NIFTY25FEB22800CE",
    '55632': "NIFTY25FEB22800PE",
    '26000': "NIFTY"
    }

instrument_tokens = [{"instrument_token": "55631", "exchange_segment": "nse_fo"}]

# Connect
client = make_connection()
def on_message(message):
    type_ = message.get('type',None)
    if type_ != 'stock_feed':
        return
    data = message['data']
    for feed in data:
        
        symbol = feed.get('tk',None)
        ltp = feed.get('ltp',None)
        ltt = feed.get('ltt',None)
        fdtm = feed.get('fdtm',None)
        if not ltt:
            ltt = fdtm
        if ltp and ltt and symbol:
            update(mapping[symbol],'1M',ltp, ltt)    
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

