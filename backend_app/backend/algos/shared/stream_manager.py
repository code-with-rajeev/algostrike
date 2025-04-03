"""
ABOUT: handles the entire process of fetching data asynchronously by creating threads and aync tasks.
Types of Streams:
    - SUB:
        subscribe to websocket stream and get realtime ticks.
        connenction lost problem solved
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
from backend.core.uttils import get_logger
from myapp.models import Algo  # ORM Model
import asyncio
import threading
import time
from datetime import datetime
import json
#from typing import Dict, Optional

logger = logging.getLogger('app')

@shared task
def start_stream_worker():
    stream_manager = StreamManager()
    stream_manager.start_stream()


class StreamManager:
    def __init__(self):
        self.key = 'active_algos:algo:requirements:SNAP'
        self.task_name = 'backend:stream_manager:GLOBAL' #task 
        self.cache = CacheManager()
        self.handler = self.cache.handler()
        self.access_token = ""  # Should be set via config or auth method
        self.server_id = ""
        self.connected = False
        self.sid = ""
        self.customer_key = os.environ.get('ADMIN_CUSTOMER_KEY') #hide in prodcution
        self.consumer_secret = os.environ.get('ADMIN_CUSTOMER_SECRET') #hide in production
        self.running = False
        self.stream = None  # Should be handled via threads

    def make_connection():
        
        client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod',
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

            # use threading to subscribe stream
            
            self.stream = Threading.thread(target = self.socket)
            stream.start()
        except Exception as a:
            # log error
            print("An error occured while logging in :", a)

    def stop_stream(self):
        """stop the streaming service"""
        pass

    def subscribe(self):
        """subscribe the intruments token"""
        pass

    def un_subscribe(self):
        """subscribe the intruments token"""
        pass

    def on_message(self, message):
        # filter recieved data, some Dict keys may be missing.
        
        if(type(message)==dict and ):
            # message: type-> Dict , data recieved from server
            
            if(message.get('type',None)=='stock_feed'):
                # Parse the data
                pass
            elif(message.get('type',None)=='quotes'):
                # Parse the data
                pass
            else:

                # May be data is recieved during login credential
                data = message.get('data',None)
                if data:
                    access_token = message.get("access_token",None)
                    if access_token:
                        self.access_token = access_token
                    server_id = message.get("server_id",None)
                    if server_id:
                        self.server_id = server_id
                        self.sid = server_id
        else:
            # message: type-> str , message recieved from server
            if(message == "Connection to the host was lost!"):
                self.connected = False
                self.reconnect()
                    
    def on_error(self, error):
        """ Handle errors """
        print("ERROR IS -> ",error)

    async def reconnect(self):
        # activate snap mode
        # try 3-5 times to re-connect
        # while self.connected != True
        # In kotak-neo, fetch any quote to re-connect.
        pass
        """
        for i in range(5):
            self.client.quotes(instrument_tokens={}, quote_type="ltp", isIndex=False,server_id='')
            time.sleep(i)
        """