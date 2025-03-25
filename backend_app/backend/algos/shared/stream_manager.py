from celery import shared_task
from myapp.models import Algo  # Adjust your ORM model
from backend.interfaces.cache_manager import CacheManager
#from backend.core.uttils import get_logger

#logger = get_logger('app')

"""
ABOUT: handles the entire process of fetching data asynchronously by creating threads.
Types of Streams:
    - SUB:
        subscribe to websocket stream and get realtime ticks.
        difficult to manage and raises connenction lost problem.
        needed to re-connent many time.
    - SNAP:
        Uses session token of user to fetch current tick at that instant.
        Fast but need to process and manage OHLC data.
    - API:
        Uses broker's public API to fetch OHLC data in date range.
        This process is delayed but accurate.
        One time fetching at specific range(recommended).
"""
from datetime import datetime
import threading
import time
class Snap:
    def __init__(self):
        self.key = 'active_algos:algo:requirements:SNAP'
        self.cache = CacheManager()
        self.tasks = {}
        self.lock = threading.Lock()
        self.start_snap()
        
        
        
    def add_snap(self,task):
        #add instrument in task
        # TYPES: offset, aligned or once
        with self.lock:
            self.tasks[task['ins']] = task['val']
            print("ADDED NEW:", task['ins'])
    def remove_snap(self,task):
        with self.lock:
            self.tasks.pop(task[ins],None)
            print("REMOVED:", task['ins'])
    def fetch_once(self,instrument):
        #fetch current data ticks
        pass
    def task(self):
        while self.running:
            with self.lock:
                for task in tasks:
                    print("DONE TASK", task['ins'])
            print()
            time.sleep(1)
    def start_snap(self):
        self.thread = threading.Thread(target = self.task, daemon = True)
        self.thread.start()
        
            
class SUB:
    pass
class API:
    pass
class StreamSubscriber:
    def __init__(self):
        self.cache = CacheManager()
        self.snap_handler = SNAP()
        
    def subscribe(mode, task={}):
        # mode = SUB/SNAP/API
        if mode == "SNAP":
            snap_mode(task)
    def snap_mode(task):
        self.snap_handler.add_snap()
    def sub_method():
        pass
    def api_method():
        pass
