"""
ABOUT: handles the entire process of fetching data asynchronously by creating threads and aync tasks.
Types of Streams:
    - SUB:
        subscribe to websocket stream and get realtime ticks.
        connection lost problem solved
    - SNAP/API:
        Uses broker's public to fetch OHLC data in date range.
        This process is delayed but accurate.
        Used to last N candles of required timeframe (recommended).
"""

"""
import required modules
"""
from celery import shared_task
from celery.schedules import crontab
from backend.interfaces.cache_manager import CacheManager
from backend.core.utils import get_logger
from websocket import WebSocketConnectionClosedException
from myapp.models import Algo  # ORM Model
import asyncio
import threading
import time
from datetime import datetime
import json
#from typing import Dict, Optional

#logger = logging.getLogger('app')

@shared task
def start_stream_worker():
    # PeriodicTask: Everyday 09:14 AM ( IST )
    stream_manager = StreamManager()
    stream_manager.start_stream()

@shared task
def stop_stream_worker():
    # PeriodicTask: Everyday 03:30 PM ( IST )
    stream_manager = StreamManager()
    stream_manager.stop_stream()

class StreamManager:
    def __init__(self):
        self.key = 'active_algos:algo:requirements:SUB'
        self.task_name = 'backend:stream_manager:GLOBAL' #task 
        self.cache = CacheManager()
        self.handler = self.cache.handler() 
        self.instrument_tokens = [{"instrument_token": "26000", "exchange_segment": "nse_cs"}] #set 'NIFTY' as default
        self.customer_key = os.environ.get('ADMIN_CUSTOMER_KEY') #hide in prodcution
        self.consumer_secret = os.environ.get('ADMIN_CUSTOMER_SECRET') #hide in production
        self.access_token = ""  # Should be set via config or auth method
        self.server_id = ""
        self.sid = ""
        self.socket_thread = None # Threads for incoming WebSocket response
        self.data_fetcher = None  # Should be injected via dependency injection
        self.connected = False
        self.running = False

    def make_connection():
        """Authenticating Credentials"""
        client = NeoAPI(consumer_key=self.consumer_key, consumer_secret=self.consumer_secret, environment='prod',
                    access_token=None, neo_fin_key=None)
        
        #Set socket listener
        client.on_message = self.on_message
        client.on_error = self.on_error
        
        client.login(mobilenumber=os.environ.get('ADMIN_NUMBER'), password=os.environ.get('ADMIN_PASSWORD'))

        client.session_2fa(OTP=os.environ.get('M_PIN'))
        return client

    def start_stream(self):
        """start the streaming service"""
        try:
            self.client = self.make_connection()
            # Update in redis
            self.running = True
            # fetch instruments from redis and update in self.token
            self.fetch_instrument_token()
            # use threading to subscribe stream           
            self.socket_thread = threading.Thread(target = self.socket)
            self.socket_thread.start()
        except Exception as a:
            # log error
            #logger.error("An error occured while logging in")
            pass

    def stop_stream(self):
        """stop the streaming service"""
        pass

    async def reconnect(self):
        # max-tries try 5 times to re-connect
        # while self.connected != True
        # In kotak-neo, fetch any quote to re-connect.
        """Asynchronously reconnect to the broker."""
        attempt = 0
        max_attempts = 5
        while not self.connected and attempt < max_attempts and self.running:
            try:
                #logger.info(f"Reconnection attempt {attempt + 1}/{max_attempts}")
                print(f"Reconnection attempt {attempt + 1}/{max_attempts}")
                # Fetch quote to force reconnect
                self.client.quotes(instrument_tokens = self.instrument_tokens, quote_type="ltp", isIndex=False,server_id=self.server_id)   
                attempt += 1
                await asyncio.sleep(attempt)  # Backoff: 1s 2s, 3s, 4s...
            except Exception as a:
                print(f"An error occoured while re-connecting : {a}")

        if not self.connected:
            logger.error("Max reconnection attempts failed. Re-login")
            self.start_stream()
        print("Reconnected successfully.")
        #logger.error("Reconnected successfully.")

    def subscribe(self):
        """subscribe the intruments token"""
        pass

    def un_subscribe(self):
        """subscribe the intruments token"""
        pass

    def on_message(self, message):
        """Handle incoming WebSocket messages."""
        # Note: filter recieved data, some Dict keys may be missing.
        
        if isinstance(message, dict):
            # message: type-> Dict , data recieved from server

            if (message.get('type',None)):
                # stock_feed / order_feed / quotes may be recieved
                if (message.get('stock_feed',None)):
                    self.connected=True
                    # Parse the data
                    feed = message['data'][0]
                    if(feed.get('ltp',None)):
                       print(f"NIFTY : {feed['ltp']}")            
                elif(message.get('quotes',None)):
                    self.connected=True
                    # Parse the data
                    print("quote: recieved")
            
            else:
                # Authentication response and access_token recieved.
                data = message.get('data',None)
                if data:
                    access_token = data.get("access_token","")
                    if access_token:
                        self.access_token = access_token
                        print("Authenticated Successfully!")
                    server_id = data.get("server_id","")
                    if server_id:
                        self.server_id = server_id
                        self.sid = server_id
                        # Both are same
                        return
                    # if sid is present
                    sid = data.get("sid","")
                    if sid:
                        self.sid = sid
                        self.server_id = sid

        elif(isinstance(message, WebSocketConnectionClosedException) and self.connected):
            # message: type-> WebSocketConnectionClosedException, 
            self.connected = False
            self.reconnect()
                    
    def on_error(self, error):
        """ Handle errors """
        print(f"Error is -> {error}")
        if(isinstance(message, WebSocketConnectionClosedException) and self.connected):
            # message: type-> WebSocketConnectionClosedException, 
            self.connected = False
            self.reconnect()

    def socket(self):
        """Connect to WebSocket"""
        self.client.subscribe(self.instrument_tokens, isIndex=False, isDepth=False)
        
    async def subscribe(self,instrument_tokens):
        """Subscribe to a streaming mode"""
        try:
            self.client.subscribe(instrument_tokens=self.instrument_tokens, isIndex=False, isDepth=False)
        except Exception as e:
            #logger.error(f"Error while subscribing: {str(e)}")
            print(f"Error while subscribing: {str(e)}")
            
    def fetch_instrument_token(self):
        """fetch all requirements from Redis"""
        try:
            cached_data = self.handler.hgetall(self.key)
            for value in cached_data.values():
                value = json.loads(value.decode('utf-8'))
                self.instrument_tokens.append({
                    "instrument_token":value['instrument_token'],
                    "exchange_segment":value['exchange_segment']
                    })
            #logger.info("Requirements loaded by StreamManager")
        except Exception as a:
            #logger.error("Could not fetch requirements by StreamManager")
            pass